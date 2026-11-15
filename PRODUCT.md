# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

delegated: plain HTML/CSS/JS served by a small FastAPI app (`coding-buddy-ui`). Fits the owner's Python stack, needs no Node build step, and keeps the Gemini API key server-side.

## Users

Primary: The thesis supervisor (Chalmers / Autoliv), watching the candidate share their screen on a Teams call. Secondary: the same supervisor opening the repo link after the call. The candidate drives the UI while talking.

## Product Purpose

Coding Buddy is a proof of concept for a master thesis: an LLM reviews R scripts used in crash-data analysis and points to errors that would change the results. The UI shows the benchmark outcome (code only vs code plus codebook) and lets the candidate paste any R script for a live review. Success: the supervisor understands in under a minute what was tested, what the numbers are, and sees one finding pinned to a real line of code.

## Positioning

Domain-grounded review: the same model is measured with and without the database codebook, on scripts with known injected errors, so the effect of domain notes is shown, not claimed.

## Operating Context

Screen-shared on Teams (compressed video, often viewed on a laptop at reduced size), so text must stay legible at small scale. Data is synthetic: synthetic crash tables, synthetic codebook, 8 scripts, one Gemini model.

## Capabilities and Constraints

- Benchmark results come from `results/results.json`, produced by `uv run coding-buddy`.
- Live review calls Gemini through the backend; the key lives in `.env` and never reaches the browser.
- Terminology: MAIS, MAIS3+, codebook, injected error, false alarm, delta-v, case weight.

## Brand Commitments

None. Autoliv and Chalmers names must not be used as branding (no logos, no implied endorsement).

## Evidence on Hand

Only the synthetic benchmark in `benchmark/` and its results. No real data, users, testimonials or production claims exist; never present the experiment as a finished result.

## Product Principles

1. Honest scale: always say "small experiment on synthetic data".
2. Evidence on the code: a finding is shown at its line, next to the ground truth.
3. One number first: the with/without codebook comparison leads.
4. Built for narration: each view supports one sentence the candidate says aloud.
