from datetime import date

import pytest

from coding_buddy.benchmark import load_cases, load_codebook
from coding_buddy.report import render_report
from coding_buddy.reviewer import Finding, build_prompt, number_lines
from coding_buddy.runner import from_json, run_benchmark, to_json
from coding_buddy.scoring import score_case, summarise


@pytest.fixture(scope="module")
def cases():
    return load_cases()


def test_manifest_resolves_every_bug_to_one_line(cases):
    assert len(cases) == 8
    assert sum(c.bug is not None for c in cases) == 6
    for case in cases:
        if case.bug:
            assert 1 <= case.bug.line <= len(case.code.splitlines())


def test_known_bug_lines(cases):
    by_name = {c.script: c for c in cases}
    assert "left_join(vehicles, by = \"crash_id\")" in by_name["01_mais3_by_vehicle_type.R"].code.splitlines()[
        by_name["01_mais3_by_vehicle_type.R"].bug.line - 1
    ]


def test_prompt_numbers_lines_and_includes_codebook_only_when_given():
    code = "a <- 1\nb <- 2"
    assert number_lines(code) == "  1 | a <- 1\n  2 | b <- 2"
    assert "<codebook>" not in build_prompt(code, None)
    assert "<codebook>\nNOTES\n</codebook>" in build_prompt(code, "NOTES")


def _finding(line: int, explanation: str = "y") -> Finding:
    return Finding(line=line, category="x", explanation=explanation)


def test_score_hit_within_tolerance_and_false_alarms(cases):
    buggy = next(c for c in cases if c.bug)
    score = score_case(buggy, [_finding(buggy.bug.line + 2), _finding(buggy.bug.line + 10)])
    assert score.found and score.false_alarms == 1

    miss = score_case(buggy, [_finding(buggy.bug.line + 3)])
    assert not miss.found and miss.false_alarms == 1


def test_explained_requires_a_diagnosis_keyword_on_a_hit(cases):
    unit = next(c for c in cases if c.script.startswith("03_"))
    right = score_case(unit, [_finding(unit.bug.line, "delta_v is already in km/h, so the factor is wrong")])
    vague = score_case(unit, [_finding(unit.bug.line, "suspicious conversion factor")])
    far = score_case(unit, [_finding(unit.bug.line + 9, "already in km/h")])
    assert right.found and right.explained
    assert vague.found and not vague.explained
    assert not far.found and not far.explained


def test_score_clean_script_counts_every_finding_as_false_alarm(cases):
    clean = next(c for c in cases if c.bug is None)
    score = score_case(clean, [_finding(1), _finding(2)])
    assert not score.has_bug and score.false_alarms == 2


class OracleReviewer:
    """Finds the bug only when the codebook is given and it needs one; flags line 1 of clean scripts."""

    name = "oracle"

    def __init__(self, cases):
        self._by_code = {c.code: c for c in cases}

    def review(self, code, codebook):
        case = self._by_code[code]
        if case.bug is None:
            return [_finding(1)]
        if case.bug.needs_codebook and codebook is None:
            return []
        return [_finding(case.bug.line, " ".join(case.bug.diagnosis_keywords[:1]))]


def test_end_to_end_with_fake_reviewer(cases):
    result = run_benchmark(OracleReviewer(cases), cases, load_codebook(), repeats=2)

    without = summarise(result.scores("without_codebook"))
    with_cb = summarise(result.scores("with_codebook"))
    assert (without.found, with_cb.found) == (3, 6)
    assert without.false_alarms_on_clean == 2

    report = render_report(result, today=date(2026, 11, 15))
    assert "| Code only | 3 / 6 | 3 / 6 |" in report
    assert "| Code + codebook | 6 / 6 | 6 / 6 |" in report
    assert "`03_risk_by_delta_v.R`" in report.split("Explained correctly more often:")[1]

    data = to_json(result)
    assert len(data["runs"]["with_codebook"]) == 2
    assert data["runs"]["with_codebook"][0][0]["found"] is True

    rescored = from_json(data, cases)
    assert summarise(rescored.scores("with_codebook")) == with_cb
