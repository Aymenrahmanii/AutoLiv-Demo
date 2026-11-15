# MAIS3+ risk by delta-v band for front-seat occupants in frontal crashes.
library(dplyr)
library(readr)

crashes   <- read_csv("data/crashes.csv")
vehicles  <- read_csv("data/vehicles.csv")
occupants <- read_csv("data/occupants.csv")

frontal <- occupants %>%
  inner_join(vehicles, by = c("crash_id", "vehicle_id")) %>%
  inner_join(crashes, by = "crash_id") %>%
  filter(crash_type == 1, seat_pos %in% c(11, 13), !is.na(mais), !is.na(delta_v))

# Express delta-v in km/h for the bands below
frontal <- frontal %>%
  mutate(delta_v_kmh = delta_v * 1.609)

risk <- frontal %>%
  mutate(dv_band = cut(delta_v_kmh, breaks = c(0, 20, 40, 60, Inf), right = FALSE)) %>%
  group_by(dv_band) %>%
  summarise(n = n(), risk_mais3 = mean(mais >= 3))

print(risk)
