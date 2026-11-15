"""Command line entry point: `uv run coding-buddy --model gemini-3.5-flash --repeats 3`."""

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from coding_buddy.benchmark import BENCHMARK_DIR, load_cases, load_codebook
from coding_buddy.report import render_report
from coding_buddy.reviewer import GeminiReviewer
from coding_buddy.runner import from_json, run_benchmark, to_json

PROJECT_DIR = BENCHMARK_DIR.parent


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the Coding Buddy R-review benchmark.")
    parser.add_argument("--model", default="gemini-3.5-flash")
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--out", type=Path, default=PROJECT_DIR / "results")
    parser.add_argument(
        "--rescore", action="store_true", help="Rescore the saved results.json and rewrite the report; no API calls."
    )
    args = parser.parse_args(argv)
    results_path = args.out / "results.json"

    if args.rescore:
        result = from_json(json.loads(results_path.read_text(encoding="utf-8")), load_cases())
    else:
        load_dotenv(PROJECT_DIR / ".env")
        result = run_benchmark(
            GeminiReviewer(args.model), load_cases(), load_codebook(), repeats=args.repeats, progress=True
        )

    args.out.mkdir(parents=True, exist_ok=True)
    results_path.write_text(json.dumps(to_json(result), indent=2), encoding="utf-8")
    (args.out / "report.md").write_text(render_report(result), encoding="utf-8")
    print(f"\nWrote {args.out / 'report.md'} and {results_path}")


if __name__ == "__main__":
    main()
