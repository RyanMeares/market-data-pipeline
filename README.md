# Market Data Pipeline

A reusable Python data pipeline for downloading and storing market and macroeconomic data for future portfolio-analysis projects.

## Goal

Build a local SQLite database containing:

- Daily adjusted stock-price data for a fixed universe of large US companies
- Company sector and industry information
- Selected macroeconomic series from FRED
- A repeatable update process with basic data-quality checks

## Data Sources

- Yahoo Finance via `yfinance`
- FRED via `fredapi`
- SEC EDGAR company facts API

## Project Structure

- `src/` - reusable Python code
- `data/` - stock universe CSV and local database
- `notebooks/` - exploratory analysis
- `tests/` - data-quality and function tests

## Current Status

- [ ] Define and save stock universe
- [ ] Create SQLite database schema
- [ ] Download stock-price data
- [ ] Add macroeconomic data
- [ ] Add update script and data checks

## How to Run

Instructions will be added as the pipeline is built.

## Notes and Limitations

The stock universe is frozen on a chosen date. Using current large-cap constituents to study older periods can introduce survivorship bias.

## Setup

Create and activate the project environment, then install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt