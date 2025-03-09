# Crypto Arbitrage Dashboard

A Streamlit web application for optimizing cryptocurrency arbitrage strategies between different platforms.

## Features

- Interactive parameter settings for capital allocation and simulation parameters
- Real-time visualization of capital growth and monthly profits
- Platform comparison with fee analysis
- Strategy optimization recommendations
- Full simulation of multi-platform arbitrage scenarios

## Setup and Installation

1. Ensure you have Python 3.8+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Run the Streamlit dashboard with:

```bash
streamlit run dashboard.py
```

The application will open in your default web browser, typically at http://localhost:8501

## Dashboard Overview

The dashboard consists of three main tabs:

1. **Simulation Parameters**: Set your initial capital, spread percentage, cycles per month, time horizon, and capital distribution across platforms.

2. **Results**: View your simulation results including:
   - Summary statistics (ending capital, total profit, return rate)
   - Capital growth charts over time
   - Monthly profit charts
   - Platform comparison table

3. **Strategy**: Get optimized strategies for multi-platform arbitrage including:
   - Capital distribution recommendations
   - Daily operational schedule
   - Maximum monthly throughput calculations

## Customization

You can modify the platform data in the dashboard.py file to reflect current fee structures and limits for each platform.
