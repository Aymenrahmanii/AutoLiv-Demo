"""Render the one-page Markdown results report."""

from datetime import date

from coding_buddy.runner import BenchmarkResult
from coding_buddy.scoring import summarise


def _num(x: float) -> str:
    return f"{x:g}" if float(x).is_integer() else f"{x:.1f}"


def _count(result: BenchmarkResult, condition: str, script: str, field: str) -> int:
    return sum(getattr(r.score, field) for run in result.runs[condition] for r in run if r.case.script == script)


def _changed(result: BenchmarkResult, cases, field: str, better: bool) -> list[str]:
    out = []
    for c in cases:
        if not c.bug:
            continue
        wo = _count(result, "without_codebook", c.script, field)
        wc = _count(result, "with_codebook", c.script, field)
        if (wc > wo) if better else (wc < wo):
            out.append(f"`{c.script}`")
    return out


def render_report(result: BenchmarkResult, today: date | None = None) -> str:
    today = today or date.today()
    without = summarise(result.scores("without_codebook"))
    with_cb = summarise(result.scores("with_codebook"))
    cases = [r.case for r in result.runs["without_codebook"][0]]
    n_clean = sum(c.bug is None for c in cases)
    reps = result.repeats
    rep_note = f", averaged over {reps} runs" if reps > 1 else ""
    n = without.n_bugs

    lines = [
        "# Coding Buddy: LLM review of R crash-analysis scripts",
        "",
        f"Small proof of concept, {today.isoformat()}. Model: `{result.model}`, temperature 0{rep_note}.",
        f"Benchmark: {len(cases)} short R scripts on synthetic crash data. {n} contain one "
        f"injected error each, {n_clean} are clean controls. Each script is reviewed twice: code only, "
        "and code plus a one-page codebook in the prompt (a minimal RAG setting).",
        "",
        "## Headline",
        "",
        "| Condition | Errors located | Correctly explained | False alarms (all) | False alarms (clean scripts) |",
        "|---|---|---|---|---|",
        f"| Code only | {_num(without.found)} / {n} | {_num(without.explained)} / {n} | "
        f"{_num(without.false_alarms)} | {_num(without.false_alarms_on_clean)} |",
        f"| Code + codebook | {_num(with_cb.found)} / {n} | {_num(with_cb.explained)} / {n} | "
        f"{_num(with_cb.false_alarms)} | {_num(with_cb.false_alarms_on_clean)} |",
        "",
        f"> Without domain notes it correctly explained {_num(without.explained)} of {n} errors; "
        f"with the codebook, {_num(with_cb.explained)}. It pointed at the right line "
        f"{_num(without.found)} and {_num(with_cb.found)} times.",
        "",
        "## Per script",
        "",
        f"Counts over {reps} run(s). L = located, E = correctly explained, FA = false alarms.",
        "",
        "| Script | Injected error | Needs codebook? | Code only (L / E) | + Codebook (L / E) | FA: code only / + codebook |",
        "|---|---|---|---|---|---|",
    ]
    for case in cases:
        bug = case.bug
        label = f"{bug.category} (line {bug.line})" if bug else "none (clean)"
        needs = ("yes" if bug.needs_codebook else "no") if bug else "-"
        cells = []
        for cond in ("without_codebook", "with_codebook"):
            if bug:
                cells.append(f"{_count(result, cond, case.script, 'found')} / {_count(result, cond, case.script, 'explained')}")
            else:
                cells.append("-")
        fa = f"{_count(result, 'without_codebook', case.script, 'false_alarms')} / {_count(result, 'with_codebook', case.script, 'false_alarms')}"
        lines.append(f"| `{case.script}` | {label} | {needs} | {cells[0]} | {cells[1]} | {fa} |")

    lines += ["", "## What changed with the codebook", ""]
    lines.append(f"- Explained correctly more often: {', '.join(_changed(result, cases, 'explained', True)) or 'none'}.")
    lines.append(f"- Explained correctly less often: {', '.join(_changed(result, cases, 'explained', False)) or 'none'}.")
    lines.append(f"- Located more often: {', '.join(_changed(result, cases, 'found', True)) or 'none'}.")
    lines += [
        "",
        "## Method and limits",
        "",
        "- Located: a finding points within ±2 lines of the injected error. Correctly explained: that finding's "
        "explanation names the actual cause (keyword list per bug in `benchmark/manifest.json`, fixed from the bug "
        "definition; when the bug is about a variable, the real variable name is required, and the 04 list was "
        "tightened to that rule after the first run). Every other finding is a false alarm, including correct remarks about uninjected issues. "
        "Raw findings are in `results.json` for manual checking.",
        "- Synthetic data, synthetic codebook, 8 scripts, one model. This is a smoke test of the idea, "
        "not a finished result.",
        "- Next steps for a thesis: real scripts and codebooks, more error types, several models, "
        "retrieval of only the relevant codebook sections, and review by domain experts.",
        "",
    ]
    return "\n".join(lines)
