# Project log

Chronological record of what was done in this repo and why. Reference article: Joas, A. (2025-02-07), *Die große Abkopplung*, FlexPower — <https://flex-power.energy/de/energieblog/die-grosse-abkopplung/>.

## 1. Understanding the original
- Article claim: German day-ahead **daily high–low spread (HL)** and the **price level** moved together for years and decoupled in 2024 (chart: 30-day moving averages, 2018–2025).
- The post does not define HL precisely. **Assumption used here:** HL = daily max − daily min of hourly day-ahead prices; price level = daily mean.

## 2. Data
- Prices: Energy-Charts API (Bundesnetzagentur | SMARD.de, CC BY 4.0), DE-LU; 2018-01…09 from DE-AT-LU (zone split on 2018-10-01). 15-minute products since Oct 2025 are averaged to hourly values.
- The API rate-limits (HTTP 429) → `src/fetch.py` retries with back-off.
- Cross-check with the dataset behind the original chart (received on request, **not redistributed**): 1,642 of 1,643 days (2020-01-01…2024-06-30) agree within 0.5 EUR/MWh; one outlier on 2024-06-26 (HL 2,325.89 in that file vs 57.85 here) looks like a data error in the file. Script: `src/compare_flexpower.py`.
- Independent plausibility check: FlexPower's Part II post (2024-03-19) states a 2023 average HL of 97.88 EUR/MWh; this repo gives 97.9.

## 3. Analysis (`src/analyze.py`, `src/season_ratio.py`)
- Daily series and 30-day moving averages, yearly table, rolling 365-day correlation, HL ÷ price ratio.
- Result 1 — reproduced and extended to Oct 2026: correlation ≈ 0.9 in 2021–23, negative (≈ −0.7) in 2025.
- Result 2 — **seasonal breakdown**: decoupling occurs in the solar season only. HL÷price in winter stays ≈ 0.8 (2018–20: 0.83, 2024–26: 0.82); in summer it rises from 0.73 to 1.80, in shoulder months from 0.98 to 1.61.
- Mechanism (hourly profiles): summer 2025 midday ≈ 7 EUR/MWh vs evening peak ≈ 143 EUR/MWh.
- Interpretation: the winter decline in HL is seasonal, the year-on-year rise of summer spreads is structural. Caveat: only two winters after the break.

## 4. Figures (`src/viz.py`, `src/viz_en.py` → `results/figures/`)
1. Overview of both series (single axis, regimes shaded)
2. Rolling correlation + HL÷price ratio
3. Monthly scatter by year (diagonal = HL equals price)
4. Seasonality heatmaps (month × year)
5. Mean hourly price profile, winter vs summer
German (`01…05`) and English (`en_01…05`) versions. Style: two hues (blue = price, orange = HL), recessive grid, direct labels, no dual axis.

## 5. Repository
- Restructured into `data/raw`, `src`, `results`, `docs`; MIT licence; `requirements.txt`; data attribution in `data/README.md`.
- The third-party dataset lives in `data/external/` and is git-ignored.
- Published on GitHub (public): <https://github.com/TimLouisWilken/de-price-decoupling>.

## 6. Open points
- HL definition remains an assumption.
- Attribution of the spread to gas price, renewable share and residual load (regression) not done.
- Other markets (FR, AT, NL, GB) are present in the original dataset but not reconstructed.
- Optional: cite the related FlexPower posts (Part II 2024-03-19, battery investment post 2025-05-22) in the README.
