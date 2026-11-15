# Coding Buddy: proof of concept

A small experiment for a master-thesis discussion: can an LLM review R scripts used in
crash-data analysis and find real mistakes, and does giving it the database codebook
(a minimal RAG setting) help?

**Current result** (`gemini-3.1-flash-lite`, 1 run, synthetic data): with or without the
codebook the model points at the right line for all 6 injected errors. But it names the
**right cause** for only 3 of 6 without the codebook, against 6 of 6 with it. Without the
codebook it blames `NA` handling instead of the unknown code `9`, and it invents column names
(`veh_id`, `person_weight`) that would not fix the script. Small experiment, not a finished result.

## What is in here

| Path | What it is |
|---|---|
| `benchmark/codebook.md` | One-page codebook of a synthetic in-depth crash database (crashes, vehicles, occupants). |
| `benchmark/scripts/*.R` | 8 short analysis scripts. 6 contain one injected error each, 2 are clean controls. |
| `benchmark/manifest.json` | Ground truth: which line holds which error, and the keywords a correct diagnosis must name. |
| `benchmark/generate_data.py` | Generates the synthetic CSVs, so the R scripts can be run if R is installed. |
| `src/coding_buddy/` | Harness: prompt + Gemini reviewer, scoring, runner, one-page report. |
| `src/coding_buddy/web/` | Demo UI: benchmark explorer and live review (FastAPI + plain HTML/CSS/JS). |
| `results/` | `report.md` (one-page results) and `results.json` (every raw finding, for manual checks). |

Injected errors: wrong join key, filter that drops valid years, unit error (km/h treated as mph),
wrong weight column, unknown code 9 averaged as a value, and uncoded injuries recoded as uninjured.

## Setup

```bash
uv sync
```

Create `.env` (git-ignored) with your key:

```
GEMINI_API_KEY=...
```

## Demo UI

```bash
uv run coding-buddy-ui
```

Open http://127.0.0.1:8000.

- **Benchmark**: the result for both conditions, every script, and the model's findings drawn as warning
  signs on the exact lines. Compare mode shows both conditions on the same lines.
- **Live review**: paste any R script and review it with or without the codebook (`Ctrl+Enter`).
  The model is `gemini-3.5-flash-lite` by default; override it with `CODING_BUDDY_MODEL`.
- **Codebook**: the domain notes the model receives.

## Run the benchmark

```bash
uv run coding-buddy --model gemini-3.1-flash-lite --repeats 1
```

Rescore saved findings after changing the ground truth (no API calls):

```bash
uv run coding-buddy --rescore
```

The Gemini free tier allows about 20 requests per model per day. One repeat needs 16 calls, so
`--repeats 3` needs a paid key or three days.

## Tests

Offline, with fake reviewers:

```bash
uv run pytest
```

## Scoring

- **Located**: a finding points within ±2 lines of the injected error.
- **Correctly explained**: a located finding whose explanation names the actual cause (keyword list per
  bug in `manifest.json`). When the bug is about a variable, the real variable name is required.
- **False alarm**: every other finding, including correct remarks about issues that were not injected.

Check `results/results.json` by hand before quoting numbers.
