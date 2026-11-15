# Belt use rate among front-seat occupants, newer vs older vehicles.
library(dplyr)
library(readr)

vehicles  <- read_csv("data/vehicles.csv")
occupants <- read_csv("data/occupants.csv")

front <- occupants %>%
  filter(seat_pos %in% c(11, 13)) %>%
  inner_join(vehicles, by = c("crash_id", "vehicle_id")) %>%
  mutate(my_group = if_else(model_year >= 2015, "2015+", "pre-2015"))

belt_rates <- front %>%
  group_by(my_group) %>%
  summarise(
    n = n(),
    belt_rate = mean(belt_use)
  )

print(belt_rates)
