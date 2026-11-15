# Codebook: synthetic in-depth crash database (SCDB)

Synthetic data, modelled loosely on in-depth crash databases. Three tables,
linked by keys. One crash has one or more vehicles; one vehicle has one or
more occupants.

## crashes.csv (one row per crash)

| Variable      | Type    | Description |
|---------------|---------|-------------|
| `crash_id`    | integer | Unique crash identifier. Primary key. |
| `crash_year`  | integer | Calendar year of the crash (2012–2023). |
| `crash_type`  | integer | 1 = frontal, 2 = side, 3 = rear, 4 = rollover, 9 = unknown. |
| `case_weight` | numeric | Sampling weight. Use it for national estimates (weighted sums / weighted means). |

## vehicles.csv (one row per vehicle)

| Variable         | Type    | Description |
|------------------|---------|-------------|
| `crash_id`       | integer | Crash the vehicle belongs to. |
| `vehicle_id`     | integer | Vehicle number **within the crash** (1, 2, ...). Not unique on its own: the key is (`crash_id`, `vehicle_id`). |
| `veh_type`       | integer | 1 = passenger car, 2 = SUV, 3 = van, 4 = truck, 9 = unknown. |
| `model_year`     | integer | Vehicle model year. |
| `vehicle_weight` | numeric | Vehicle curb mass in **kg**. A physical property, not a sampling weight. |
| `delta_v`        | numeric | Change of velocity during the crash, already in **km/h**. Missing (NA) when not reconstructed. |

## occupants.csv (one row per occupant)

| Variable      | Type    | Description |
|---------------|---------|-------------|
| `crash_id`    | integer | Crash identifier. |
| `vehicle_id`  | integer | Vehicle number within the crash. The key to `vehicles.csv` is (`crash_id`, `vehicle_id`). |
| `occupant_id` | integer | Occupant number within the vehicle. |
| `age`         | integer | Age in years. 999 = unknown. |
| `sex`         | integer | 1 = male, 2 = female, 9 = unknown. |
| `seat_pos`    | integer | 11 = driver, 13 = front passenger, 21–23 = second row, 99 = unknown. |
| `belt_use`    | integer | 0 = not belted, 1 = belted, 9 = unknown. |
| `mais`        | integer | Maximum AIS injury severity, 0 (uninjured) to 6. NA = injury not coded (not the same as uninjured). |

## Analysis conventions

- "Serious injury" means `mais >= 3` (MAIS3+).
- Occupants whose injury is not coded (`mais` is NA) are **excluded** from injury-risk
  denominators. They must never be counted as uninjured.
- Code 9 (and 99 / 999) means unknown and must be excluded before computing
  rates, proportions or means of that variable.
- Study periods are inclusive of both end years.
