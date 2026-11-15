"""Score reviewer findings against the injected bugs."""

from dataclasses import dataclass

from coding_buddy.benchmark import Case, InjectedBug
from coding_buddy.reviewer import Finding

LINE_TOLERANCE = 2


@dataclass(frozen=True)
class CaseScore:
    script: str
    has_bug: bool
    found: bool  # some finding points within tolerance of the injected line
    false_alarms: int
    explained: bool = False  # a hit whose explanation names the actual cause


def is_hit(finding: Finding, bug: InjectedBug, tolerance: int = LINE_TOLERANCE) -> bool:
    return abs(finding.line - bug.line) <= tolerance


def is_explained(finding: Finding, bug: InjectedBug) -> bool:
    text = finding.explanation.lower()
    return any(k.lower() in text for k in bug.diagnosis_keywords)


def score_case(case: Case, findings: list[Finding], tolerance: int = LINE_TOLERANCE) -> CaseScore:
    """A finding within `tolerance` lines of the injected bug counts as a hit; every other finding is a false alarm."""
    if case.bug is None:
        return CaseScore(case.script, has_bug=False, found=False, false_alarms=len(findings))
    hits = [f for f in findings if is_hit(f, case.bug, tolerance)]
    return CaseScore(
        case.script,
        has_bug=True,
        found=bool(hits),
        false_alarms=len(findings) - len(hits),
        explained=any(is_explained(f, case.bug) for f in hits),
    )


@dataclass(frozen=True)
class Summary:
    n_bugs: int
    found: float
    explained: float
    false_alarms: float
    false_alarms_on_clean: float


def summarise(runs: list[list[CaseScore]]) -> Summary:
    """Average over repeated runs; each run is the list of case scores for one pass over the benchmark."""
    n = len(runs)
    return Summary(
        n_bugs=sum(s.has_bug for s in runs[0]),
        found=sum(s.found for run in runs for s in run) / n,
        explained=sum(s.explained for run in runs for s in run) / n,
        false_alarms=sum(s.false_alarms for run in runs for s in run) / n,
        false_alarms_on_clean=sum(s.false_alarms for run in runs for s in run if not s.has_bug) / n,
    )
