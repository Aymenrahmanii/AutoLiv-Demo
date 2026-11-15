"""Demo UI backend: serves the page, the benchmark results, and a live review endpoint.

Run with `uv run coding-buddy-ui` and open http://127.0.0.1:8000.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from coding_buddy.benchmark import BENCHMARK_DIR, Case, load_cases, load_codebook
from coding_buddy.reviewer import Finding, GeminiReviewer, Reviewer
from coding_buddy.runner import from_json
from coding_buddy.scoring import CaseScore, is_explained, is_hit, summarise

WEB_DIR = Path(__file__).parent
PROJECT_DIR = BENCHMARK_DIR.parent
RESULTS_PATH = PROJECT_DIR / "results" / "results.json"
DEFAULT_MODEL = "gemini-3.5-flash-lite"  # fast enough for a live demo; override with CODING_BUDDY_MODEL
MAX_SCRIPT_CHARS = 20_000


class ReviewRequest(BaseModel):
    code: str = Field(min_length=1, max_length=MAX_SCRIPT_CHARS)
    use_codebook: bool = True


class ReviewResponse(BaseModel):
    model: str
    findings: list[Finding]


def _case_payload(case: Case) -> dict:
    bug = case.bug
    return {
        "script": case.script,
        "code": case.code,
        "bug": None
        if bug is None
        else {
            "line": bug.line,
            "category": bug.category,
            "description": bug.description,
            "needs_codebook": bug.needs_codebook,
        },
    }


def _summary(scores: list[list[CaseScore]]) -> dict:
    s = summarise(scores)
    return {
        "n_bugs": s.n_bugs,
        "found": s.found,
        "explained": s.explained,
        "false_alarms": s.false_alarms,
        "false_alarms_on_clean": s.false_alarms_on_clean,
    }


def benchmark_payload(results_path: Path = RESULTS_PATH) -> dict:
    """Cases plus saved findings, rescored with the current ground truth so the UI never disagrees with the report."""
    cases = load_cases()
    payload: dict = {"cases": [_case_payload(c) for c in cases], "results": None}
    if not results_path.exists():
        return payload
    result = from_json(json.loads(results_path.read_text(encoding="utf-8")), cases)
    runs = {}
    for cond, cond_runs in result.runs.items():
        runs[cond] = [
            [
                {
                    "script": r.case.script,
                    "found": r.score.found,
                    "explained": r.score.explained,
                    "false_alarms": r.score.false_alarms,
                    "findings": [
                        {
                            **f.model_dump(),
                            "hit": bool(r.case.bug and is_hit(f, r.case.bug)),
                            "explained": bool(r.case.bug and is_hit(f, r.case.bug) and is_explained(f, r.case.bug)),
                        }
                        for f in r.findings
                    ],
                }
                for r in run
            ]
            for run in cond_runs
        ]
    payload["results"] = {
        "model": result.model,
        "repeats": result.repeats,
        "runs": runs,
        "summary": {cond: _summary(result.scores(cond)) for cond in result.runs},
    }
    return payload


def create_app(reviewer: Reviewer | None = None, results_path: Path = RESULTS_PATH) -> FastAPI:
    load_dotenv(PROJECT_DIR / ".env")
    app = FastAPI(title="Coding Buddy", docs_url=None, redoc_url=None)
    state: dict = {"reviewer": reviewer}

    def get_reviewer() -> Reviewer:
        if state["reviewer"] is None:
            if not os.environ.get("GEMINI_API_KEY"):
                raise HTTPException(503, "GEMINI_API_KEY is not set. Add it to .env and restart the server.")
            state["reviewer"] = GeminiReviewer(os.environ.get("CODING_BUDDY_MODEL", DEFAULT_MODEL), max_retries=2)
        return state["reviewer"]

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(WEB_DIR / "index.html")

    @app.get("/api/benchmark")
    def benchmark() -> dict:
        return benchmark_payload(results_path)

    @app.get("/api/codebook")
    def codebook() -> dict:
        return {"markdown": load_codebook()}

    @app.post("/api/review")
    def review(req: ReviewRequest) -> ReviewResponse:
        rev = get_reviewer()
        try:
            findings = rev.review(req.code, load_codebook() if req.use_codebook else None)
        except Exception as exc:  # surface the provider error to the UI instead of a bare 500
            raise HTTPException(502, f"The model call failed: {str(exc)[:300]}") from exc
        return ReviewResponse(model=rev.name, findings=sorted(findings, key=lambda f: f.line))

    app.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")
    return app


def main() -> None:
    import uvicorn

    uvicorn.run(create_app(), host="127.0.0.1", port=int(os.environ.get("PORT", "8000")))
