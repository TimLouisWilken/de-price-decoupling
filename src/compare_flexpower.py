"""Optional cross-check against the FlexPower dataset (not redistributed; place at data/external/)."""
import pandas as pd, sys
p = "data/external/HL_BASE_DE_FR_AT_NL_GB_dataset.xlsx"
f = pd.read_excel(p, sheet_name=1).iloc[:, :13]
f["time"] = pd.to_datetime(f.time, errors="coerce"); f = f.dropna(subset=["time"]).set_index("time")
d = pd.read_csv("results/daily.csv", index_col=0, parse_dates=True)
j = f[["HL_DE", "BASE_DE"]].join(d[["hl", "mean"]], how="inner")
bad = j[((j.HL_DE - j.hl).abs() > .5) | ((j.BASE_DE - j["mean"]).abs() > .5)]
print(f"{len(j)} days compared, {len(j) - len(bad)} match within 0.5 EUR/MWh"); print(bad)
