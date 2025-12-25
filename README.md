# Data Cleaning Mini Sample (Python)

This repository provides a small, self-contained example of a data-cleaning workflow using a public dataset.

## What’s included
- `src/clean.py` — cleaning script (column name normalization, type coercion, basic validity flags)
- `output/qa_report.md` — short QA summary (missingness + basic checks)
- `output/data_dictionary.csv` — simple data dictionary (dtype, missing rate, example value)
- `data/raw/` — raw data + a small raw sample
- `data/processed/` — cleaned data + a small processed sample

## Data
Raw data file:
- `data/raw/ta9_data.csv`

Processed outputs:
- `data/processed/ta9_data_clean.csv`
- `data/processed/sample_processed_200.csv`

## Notes
- The goal of this repo is to demonstrate data management and cleaning practices (consistent naming, type handling, and basic QA checks).
- If you reuse this structure for other projects, replace the raw input under `data/raw/` and adjust the variable-specific rules in `src/clean.py`.

## Author
Yichen Huang
