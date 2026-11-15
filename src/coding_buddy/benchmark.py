"""Load the benchmark: R scripts plus the ground truth of which line holds the injected error."""

import json
from dataclasses import dataclass
from pathlib import Path

BENCHMARK_DIR = Path(__file__).resolve().parents[2] / "benchmark"


@dataclass(frozen=True)
class InjectedBug:
    category: str
    line: int
    description: str
    needs_codebook: bool
    diagnosis_keywords: tuple[str, ...] = ()


@dataclass(frozen=True)
class Case:
    script: str
    code: str
    bug: InjectedBug | None


def _line_of(snippet: str, code: str, script: str) -> int:
    matches = [i for i, line in enumerate(code.splitlines(), start=1) if snippet in line]
    if len(matches) != 1:
        raise ValueError(f"{script}: snippet {snippet!r} must match exactly one line, matched {len(matches)}")
    return matches[0]


def load_cases(benchmark_dir: Path = BENCHMARK_DIR) -> list[Case]:
    manifest = json.loads((benchmark_dir / "manifest.json").read_text(encoding="utf-8"))
    cases = []
    for entry in manifest["cases"]:
        code = (benchmark_dir / "scripts" / entry["script"]).read_text(encoding="utf-8")
        raw_bug = entry["bug"]
        bug = None
        if raw_bug is not None:
            bug = InjectedBug(
                category=raw_bug["category"],
                line=_line_of(raw_bug["snippet"], code, entry["script"]),
                description=raw_bug["description"],
                needs_codebook=raw_bug["needs_codebook"],
                diagnosis_keywords=tuple(raw_bug.get("diagnosis_keywords", ())),
            )
        cases.append(Case(script=entry["script"], code=code, bug=bug))
    return cases


def load_codebook(benchmark_dir: Path = BENCHMARK_DIR) -> str:
    return (benchmark_dir / "codebook.md").read_text(encoding="utf-8")
