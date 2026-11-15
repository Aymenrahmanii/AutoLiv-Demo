# Yearly weighted number of seriously injured (MAIS3+) occupants,
# study period 2015-2022.
library(dplyr)
library(readr)

crashes   <- read_csv("data/crashes.csv")
occupants <- read_csv("data/occupants.csv")

serious <- occupants %>%
  filter(!is.na(mais), mais >= 3) %>%
  inner_join(crashes, by = "crash_id")

trend <- serious %>%
  filter(crash_year > 2015 & crash_year < 2022) %>%
  group_by(crash_year) %>%
  summarise(
    n_serious = n(),
    weighted_serious = sum(case_weight)
  )

write_csv(trend, "output/serious_trend_2015_2022.csv")
