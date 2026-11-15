"""Run the reviewer over every script, with and without the codebook."""

from dataclasses import dataclass, field

from coding_buddy.benchmark import Case
from coding_buddy.reviewer import Finding, Reviewer
from coding_buddy.scoring import CaseScore, score_case

CONDITIONS = ("without_codebook", "with_codebook")


@dataclass
class CaseResult:
    case: Case
    findings: list[Finding]
    score: CaseScore


@dataclass
class BenchmarkResult:
    model: str
    repeats: int
    # condition -> one list of case results per repeat
    runs: dict[str, list[list[CaseResult]]] = field(default_factory=dict)

    def scores(self, condition: str) -> list[list[CaseScore]]:
        return [[r.score for r in run] for run in self.runs[condition]]


def run_benchmark(
    reviewer: Reviewer,
    cases: list[Case],
    codebook: str,
    repeats: int = 1,
    progress: bool = False,
) -> BenchmarkResult:
    result = BenchmarkResult(model=reviewer.name, repeats=repeats)
    for condition in CONDITIONS:
        notes = codebook if condition == "with_codebook" else None
        result.runs[condition] = []
        for rep in range(repeats):
            run = []
            for case in cases:
                findings = reviewer.review(case.code, notes)
                run.append(CaseResult(case, findings, score_case(case, findings)))
                if progress:
                    print(f"[{condition} {rep + 1}/{repeats}] {case.script}: {len(findings)} finding(s)")
            result.runs[condition].append(run)
    return result


def from_json(data: dict, cases: list[Case]) -> BenchmarkResult:
    """Rebuild a result from saved findings and rescore it with the current ground truth (no API calls)."""
    by_script = {c.script: c for c in cases}
    result = BenchmarkResult(model=data["model"], repeats=data["repeats"])
    for condition, runs in data["runs"].items():
        result.runs[condition] = []
        for run in runs:
            rows = []
            for row in run:
                case = by_script[row["script"]]
                findings = [Finding.model_validate(f) for f in row["findings"]]
                rows.append(CaseResult(case, findings, score_case(case, findings)))
            result.runs[condition].append(rows)
    return result


def to_json(result: BenchmarkResult) -> dict:
    """Everything needed to re-check the automatic scoring by hand."""
    return {
        "model": result.model,
        "repeats": result.repeats,
        "runs": {
            condition: [
                [
                    {
                        "script": r.case.script,
                        "injected_bug_line": r.case.bug.line if r.case.bug else None,
                        "found": r.score.found,
                        "explained": r.score.explained,
                        "false_alarms": r.score.false_alarms,
                        "findings": [f.model_dump() for f in r.findings],
                    }
                    for r in run
                ]
                for run in runs
            ]
            for condition, runs in result.runs.items()
        },
    }
