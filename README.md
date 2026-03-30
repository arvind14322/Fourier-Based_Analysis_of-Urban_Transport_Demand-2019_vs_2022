# Fourier-Based Analysis of Urban Transport Demand: 2019 vs 2022

## Overview

This repository contains an analytical study of urban public transport demand in 2019 and 2022. The project combines daily aggregate data (2019) with journey-level records (2022) and uses Fourier series, regression, and descriptive statistics to compare demand patterns across years.

The analysis focuses on buses and metro services in 2019 and metro journeys in 2022, with 2022 totals scaled to make them comparable to 2019. The work was completed as part of a statistics and trends assignment.

## Data

- **2019data1.csv** – Daily totals for bus and metro, including:
  - Peak and off‑peak passenger counts
  - Peak and off‑peak revenue
  - Separate fields for bus and metro
- **2022data1.csv** – Journey-level records for 2022, including:
  - Date and time of each trip
  - Mode (Metro)
  - Distance and duration
  - Ticket price

The 2022 journey-level data is aggregated to daily totals and then scaled to match the 2019 demand level so that seasonal patterns can be compared on the same scale.

## Methods

The analysis script performs the following steps:

- Reads and preprocesses the 2019 and 2022 datasets.
- Constructs day-of-year and weekday indicators for both years.
- Aggregates 2022 journeys to daily passenger totals and computes scaling factors to align 2022 totals with 2019.
- Builds 8-term Fourier series models for the daily passenger totals in 2019 and scaled 2022.
- Computes weekday averages (Monday–Sunday) for both years.
- Classifies 2022 journeys as:
  - Peak weekday (e.g., 7–9 and 16–18 on workdays)
  - Off‑peak weekday
  - Weekend
- Estimates revenue contributions from peak, off‑peak, and weekend travel in 2022 and derives the fractions X, Y, and Z of total revenue.
- Fits a simple linear regression model of metro ticket price as a function of distance for 2022.

## Figures

The script generates several figures:

1. **Figure 1 – Daily passenger totals and 8-term Fourier curves**  
   - Scatter points for 2019 daily totals and scaled 2022 daily totals.  
   - Smooth 8-term Fourier curves for both years on a common y-axis (millions of passengers).

2. **Figure 2 – Average weekday totals (log scale)**  
   - Bar chart of mean passengers by weekday (Mon–Sun) for 2019 and scaled 2022.  
   - Logarithmic y-axis to highlight differences across weekdays.  
   - Text annotation showing the revenue fractions X (peak weekdays), Y (off‑peak weekdays), and Z (weekends) for 2022.

3. **Figure 3 – Metro ticket price vs distance (2022)**  
   - Scatter plot of distance versus ticket price for metro journeys in 2022.  
   - Fitted regression line with the estimated equation printed in the plot.

4. **Figure 4 – Peak, off‑peak, and weekend passenger totals**  
   - Bar chart comparing 2019 vs scaled 2022 totals for:
     - Peak weekdays
     - Off‑peak weekdays
     - Weekends  
   - Text annotation with the same revenue fractions (X, Y, Z).

5. **Figure 5 – Bus passengers per day (July 2019)**  
   - Bar chart of total bus passengers (peak + off‑peak) for each day in July 2019.  
   - Includes labelled axes, daily ticks, and a light grid for readability.

## Key Insights (High-Level)

- Fourier smoothing highlights seasonal demand patterns across the year for both 2019 and 2022.
- Weekday averages show how typical daily demand differs between weekdays and weekends, and how 2022 compares to 2019 after scaling.
- The regression of metro price against distance provides an approximate fare rule for 2022 metro journeys.
- Peak, off‑peak, and weekend comparisons illustrate how demand and revenue are distributed across time-of-day and day-of-week categories.

## Getting Started

To run the analysis locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/arvind14322/Fourier-Based_Analysis_of-Urban_Transport_Demand-2019_vs_2022.git
   cd Fourier-Based_Analysis_of-Urban_Transport_Demand-2019_vs_2022
   ```
2. Create and activate a Python virtual environment (optional but recommended).
3. Install required packages (for example: `numpy`, `pandas`, `matplotlib`):
   ```bash
   pip install numpy pandas matplotlib
   ```
4. Run the analysis script:
   ```bash
   python temp.py
   ```

The script will compute all statistics and display the figures.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
