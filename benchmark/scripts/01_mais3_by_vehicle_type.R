# Proportion of belted occupants with MAIS3+ injuries, by vehicle type.
library(dplyr)
library(readr)

occupants <- read_csv("data/occupants.csv")
vehicles  <- read_csv("data/vehicles.csv")

# Attach vehicle information to each occupant
occ_veh <- occupants %>%
  left_join(vehicles, by = "crash_id")

result <- occ_veh %>%
  filter(belt_use == 1, !is.na(mais), veh_type != 9) %>%
  mutate(serious = mais >= 3) %>%
  group_by(veh_type) %>%
  summarise(
    n_occupants = n(),
    share_mais3 = mean(serious)
  )

print(result)
