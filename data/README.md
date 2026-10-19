# Data
- `raw/de_lu_day_ahead.csv` – Day-ahead auction prices (EUR/MWh, UTC timestamps), bidding zone DE-LU from 2018-10-01, DE-AT-LU before. Source: [Energy-Charts](https://api.energy-charts.info/) (Fraunhofer ISE), data from Bundesnetzagentur | SMARD.de, licence CC BY 4.0. Hourly until 2025-09, 15-minute since 2025-10 (aggregated to hourly in `src/analyze.py`). Re-create with `src/fetch.py`.
- `external/` – (git-ignored) FlexPower dataset `HL_BASE_DE_FR_AT_NL_GB_dataset.xlsx`, received on request; not redistributed. Only used by `src/compare_flexpower.py`.
