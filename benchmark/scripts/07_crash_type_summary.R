# Crash counts and weighted shares by crash type, excluding unknown type.
library(dplyr)
library(readr)

crashes <- read_csv("data/crashes.csv")

type_labels <- c(`1` = "frontal", `2` = "side", `3` = "rear", `4` = "rollover")

summary_by_type <- crashes %>%
  filter(crash_type != 9) %>%
  mutate(type = unname(type_labels[as.character(crash_type)])) %>%
  group_by(type) %>%
  summarise(
    n_crashes = n(),
    weighted_crashes = sum(case_weight)
  ) %>%
  mutate(weighted_share = weighted_crashes / sum(weighted_crashes))

print(summary_by_type)
