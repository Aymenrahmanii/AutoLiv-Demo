# National estimate of the MAIS3+ share among passenger-car drivers,
# using the sampling weights.
library(dplyr)
library(readr)

vehicles  <- read_csv("data/vehicles.csv")
occupants <- read_csv("data/occupants.csv")

drivers <- occupants %>%
  filter(seat_pos == 11, !is.na(mais)) %>%
  inner_join(vehicles, by = c("crash_id", "vehicle_id")) %>%
  filter(veh_type == 1) %>%
  mutate(serious = as.numeric(mais >= 3))

estimate <- drivers %>%
  summarise(
    n_drivers = n(),
    weighted_share_mais3 = weighted.mean(serious, w = vehicle_weight)
  )

print(estimate)
