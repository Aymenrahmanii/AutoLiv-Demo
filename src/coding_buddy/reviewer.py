"""LLM code reviewer: builds the review prompt and calls Gemini for structured findings."""

import time
from typing import Protocol

from pydantic import BaseModel, Field

SYSTEM_PROMPT = """You review R scripts written for traffic-safety research on crash data.
Report only errors that would change the analysis results: wrong joins, filters that \
drop or keep the wrong rows, unit errors, wrong columns, mishandled missing or unknown \
values, wrong calculations. Do not report style, performance, or missing comments.
If the script is correct, return an empty list of findings. Do not invent problems."""


class Finding(BaseModel):
    line: int = Field(description="Line number (as numbered in the prompt) where the error is.")
    category: str = Field(description="Short label, e.g. wrong_join_key, unit_error, missing_values.")
    explanation: str = Field(description="One or two sentences: what is wrong and why it changes the result.")


class ReviewOutput(BaseModel):
    findings: list[Finding]


class Reviewer(Protocol):
    name: str

    def review(self, code: str, codebook: str | None) -> list[Finding]: ...


def number_lines(code: str) -> str:
    return "\n".join(f"{i:>3} | {line}" for i, line in enumerate(code.splitlines(), start=1))


def build_prompt(code: str, codebook: str | None) -> str:
    parts = []
    if codebook:
        parts.append(f"Codebook of the database the script uses:\n<codebook>\n{codebook}\n</codebook>")
    parts.append(f"Review this R script. Line numbers are shown before `|`.\n<script>\n{number_lines(code)}\n</script>")
    return "\n\n".join(parts)


class GeminiReviewer:
    """Calls the Gemini API with a JSON response schema. Reads GEMINI_API_KEY from the environment."""

    def __init__(self, model: str, max_retries: int = 5, timeout_s: float = 90) -> None:
        from google import genai
        from google.genai import types

        self.name = model
        # Without a timeout a stalled request blocks the whole benchmark forever.
        self._client = genai.Client(http_options=types.HttpOptions(timeout=int(timeout_s * 1000)))
        self._max_retries = max_retries

    def review(self, code: str, codebook: str | None) -> list[Finding]:
        from google.genai import errors, types

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.0,
            response_mime_type="application/json",
            response_schema=ReviewOutput,
        )
        for attempt in range(self._max_retries):
            try:
                response = self._client.models.generate_content(
                    model=self.name, contents=build_prompt(code, codebook), config=config
                )
                break
            except errors.APIError as exc:
                # A daily quota resets in hours; retrying only burns time.
                daily_quota = exc.code == 429 and "PerDay" in str(exc)
                retryable = exc.code in (429, 500, 503, 504) and not daily_quota
                if not retryable or attempt == self._max_retries - 1:
                    raise
                time.sleep(2 ** attempt * 5)
        parsed = response.parsed
        if isinstance(parsed, ReviewOutput):
            return parsed.findings
        return ReviewOutput.model_validate_json(response.text or '{"findings": []}').findings
