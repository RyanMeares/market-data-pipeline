library(tidyverse)
library(fredr)
library(quantmod)

# Load your private FRED key from the existing .env file.
readRenviron(".env")
fredr_set_key(Sys.getenv("FRED_API_KEY"))

if (Sys.getenv("FRED_API_KEY") == "") {
  stop("FRED_API_KEY was not found. Check your .env file.")
}

# 1. Pull a FRED series: unemployment rate.
unrate <- fredr(
  series_id = "UNRATE",
  observation_start = as.Date("2015-01-01")
)

# 2. Make a ggplot2 chart and save it.
unrate_chart <- ggplot(unrate, aes(x = date, y = value)) +
  geom_line(color = "steelblue", linewidth = 0.8) +
  labs(
    title = "US Unemployment Rate",
    x = "Date",
    y = "Percent"
  ) +
  theme_minimal()

print(unrate_chart)

ggsave(
  filename = "notebooks/unemployment_rate.png",
  plot = unrate_chart,
  width = 8,
  height = 4
)

# 3. Reshape wide data into long data with pivot_longer().
wide_example <- tibble(
  region = c("Northeast", "South", "Midwest"),
  unemployment_2024 = c(4.0, 3.7, 3.9),
  unemployment_2025 = c(4.2, 3.8, 4.1)
)

long_example <- wide_example |>
  pivot_longer(
    cols = starts_with("unemployment_"),
    names_to = "year",
    values_to = "unemployment_rate"
  )

print(long_example)

# 4. Fit a simple time-trend regression with lm().
unrate_model_data <- unrate |>
  mutate(time_index = row_number())

unrate_model <- lm(value ~ time_index, data = unrate_model_data)

print(summary(unrate_model))

# 5. Use group_by() and summarise() on your stock universe.
universe <- read_csv("data/universe.csv", show_col_types = FALSE)

sector_summary <- universe |>
  group_by(sector) |>
  summarise(number_of_stocks = n(), .groups = "drop") |>
  arrange(desc(number_of_stocks))

print(sector_summary)

# 6. Pull stock prices with quantmod and compute daily returns.
aapl_prices <- getSymbols(
  "AAPL",
  src = "yahoo",
  from = "2020-01-01",
  auto.assign = FALSE
)

aapl_returns <- dailyReturn(Ad(aapl_prices))

print(head(aapl_returns))

write_csv(
  tibble(
    date = as.Date(index(aapl_returns)),
    daily_return = as.numeric(aapl_returns)
  ),
  "data/aapl_daily_returns.csv"
)

print("Phase 0b R fluency sprint completed.")