# Coding Buddy: LLM review of R crash-analysis scripts

Small proof of concept, 2026-11-15. Model: `gemini-3.1-flash-lite`, temperature 0.
Benchmark: 8 short R scripts on synthetic crash data. 6 contain one injected error each, 2 are clean controls. Each script is reviewed twice: code only, and code plus a one-page codebook in the prompt (a minimal RAG setting).

## Headline

| Condition | Errors located | Correctly explained | False alarms (all) | False alarms (clean scripts) |
|---|---|---|---|---|
| Code only | 6 / 6 | 3 / 6 | 1 | 1 |
| Code + codebook | 6 / 6 | 6 / 6 | 1 | 0 |

> Without domain notes it correctly explained 3 of 6 errors; with the codebook, 6. It pointed at the right line 6 and 6 times.

## Per script

Counts over 1 run(s). L = located, E = correctly explained, FA = false alarms.

| Script | Injected error | Needs codebook? | Code only (L / E) | + Codebook (L / E) | FA: code only / + codebook |
|---|---|---|---|---|---|
| `01_mais3_by_vehicle_type.R` | wrong_join_key (line 10) | no | 1 / 0 | 1 / 1 | 0 / 0 |
| `02_serious_trend_2015_2022.R` | filter_drops_valid_rows (line 14) | no | 1 / 1 | 1 / 1 | 0 / 0 |
| `03_risk_by_delta_v.R` | unit_error (line 16) | yes | 1 / 1 | 1 / 1 | 0 / 0 |
| `04_weighted_driver_estimate.R` | wrong_column (line 18) | yes | 1 / 0 | 1 / 1 | 0 / 1 |
| `05_belt_rate_by_model_year.R` | unknown_code_not_excluded (line 17) | yes | 1 / 0 | 1 / 1 | 0 / 0 |
| `06_risk_by_age_group.R` | missing_values (line 10) | no | 1 / 1 | 1 / 1 | 0 / 0 |
| `07_crash_type_summary.R` | none (clean) | - | - | - | 1 / 0 |
| `08_belt_age_logistic_model.R` | none (clean) | - | - | - | 0 / 0 |

## What changed with the codebook

- Explained correctly more often: `01_mais3_by_vehicle_type.R`, `04_weighted_driver_estimate.R`, `05_belt_rate_by_model_year.R`.
- Explained correctly less often: none.
- Located more often: none.

## Method and limits

- Located: a finding points within ±2 lines of the injected error. Correctly explained: that finding's explanation names the actual cause (keyword list per bug in `benchmark/manifest.json`, fixed from the bug definition; when the bug is about a variable, the real variable name is required, and the 04 list was tightened to that rule after the first run). Every other finding is a false alarm, including correct remarks about uninjected issues. Raw findings are in `results.json` for manual checking.
- Synthetic data, synthetic codebook, 8 scripts, one model. This is a smoke test of the idea, not a finished result.
- Next steps for a thesis: real scripts and codebooks, more error types, several models, retrieval of only the relevant codebook sections, and review by domain experts.
