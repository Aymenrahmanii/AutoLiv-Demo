# MAIS3+ risk by age group for all occupants.
library(dplyr)
library(readr)
library(tidyr)

occupants <- read_csv("data/occupants.csv")

risk_by_age <- occupants %>%
  filter(age != 999) %>%
  replace_na(list(mais = 0)) %>%
  mutate(
    age_group = cut(age, breaks = c(0, 18, 30, 50, 65, Inf), right = FALSE),
    serious = mais >= 3
  ) %>%
  group_by(age_group) %>%
  summarise(n = n(), risk_mais3 = mean(serious))

print(risk_by_age)
