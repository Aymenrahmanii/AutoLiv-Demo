# Exploratory (unweighted) logistic regression: MAIS3+ vs belt use and age,
# front-seat occupants of passenger cars.
library(dplyr)
library(readr)

vehicles  <- read_csv("data/vehicles.csv")
occupants <- read_csv("data/occupants.csv")

model_data <- occupants %>%
  inner_join(vehicles, by = c("crash_id", "vehicle_id")) %>%
  filter(
    veh_type == 1,
    seat_pos %in% c(11, 13),
    belt_use %in% c(0, 1),
    age != 999,
    !is.na(mais)
  ) %>%
  mutate(
    serious = as.integer(mais >= 3),
    belted  = factor(belt_use, levels = c(0, 1), labels = c("unbelted", "belted"))
  )

fit <- glm(serious ~ belted + age, family = binomial(), data = model_data)
summary(fit)

# Odds ratios with 95% confidence intervals
exp(cbind(OR = coef(fit), confint.default(fit)))
