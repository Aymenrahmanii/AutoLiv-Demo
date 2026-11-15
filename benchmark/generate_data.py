"""Generate the synthetic crash tables described in codebook.md.

The benchmark only sends R source to the LLM, so the data is not needed to run it.
It exists so the R scripts can actually be executed if R is installed.

Usage: uv run python benchmark/generate_data.py [--crashes 500] [--seed 7]
"""

import argparse
import csv
import random
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def _write(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(["NA" if v is None else v for v in row] for row in rows)


def _maybe_unknown(rng: random.Random, value: int, code: int, p: float) -> int:
    return code if rng.random() < p else value


def generate(n_crashes: int, seed: int) -> None:
    rng = random.Random(seed)
    crashes, vehicles, occupants = [], [], []
    seats = [11, 13, 21, 22, 23]

    for crash_id in range(1, n_crashes + 1):
        crash_type = _maybe_unknown(rng, rng.choice([1, 1, 2, 3, 4]), 9, 0.03)
        crashes.append([crash_id, rng.randint(2012, 2023), crash_type, round(rng.uniform(5, 200), 2)])

        for vehicle_id in range(1, rng.choice([1, 2, 2, 3]) + 1):
            delta_v = None if rng.random() < 0.15 else round(rng.gammavariate(4, 7), 1)
            vehicles.append([
                crash_id,
                vehicle_id,
                _maybe_unknown(rng, rng.choice([1, 1, 1, 2, 3, 4]), 9, 0.02),
                rng.randint(2000, 2023),
                rng.randint(900, 2600),
                delta_v,
            ])

            for occupant_id, seat in enumerate(seats[: rng.randint(1, 4)], start=1):
                belted = 1 if rng.random() < 0.85 else 0
                severity_bias = (delta_v or 25) / 25 + (0 if belted else 1.5)
                mais = min(6, int(rng.expovariate(1 / severity_bias)))
                occupants.append([
                    crash_id,
                    vehicle_id,
                    occupant_id,
                    _maybe_unknown(rng, rng.randint(1, 90), 999, 0.04),
                    _maybe_unknown(rng, rng.choice([1, 2]), 9, 0.02),
                    _maybe_unknown(rng, seat, 99, 0.02),
                    _maybe_unknown(rng, belted, 9, 0.10),
                    None if rng.random() < 0.08 else mais,
                ])

    DATA_DIR.mkdir(exist_ok=True)
    _write(DATA_DIR / "crashes.csv", ["crash_id", "crash_year", "crash_type", "case_weight"], crashes)
    _write(
        DATA_DIR / "vehicles.csv",
        ["crash_id", "vehicle_id", "veh_type", "model_year", "vehicle_weight", "delta_v"],
        vehicles,
    )
    _write(
        DATA_DIR / "occupants.csv",
        ["crash_id", "vehicle_id", "occupant_id", "age", "sex", "seat_pos", "belt_use", "mais"],
        occupants,
    )
    print(f"Wrote {len(crashes)} crashes, {len(vehicles)} vehicles, {len(occupants)} occupants to {DATA_DIR}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--crashes", type=int, default=500)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    generate(args.crashes, args.seed)


if __name__ == "__main__":
    main()
