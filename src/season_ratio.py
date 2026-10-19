"""HL / price ratio by period and season -> results/season_ratio.csv"""
import pandas as pd
d = pd.read_csv("results/daily.csv", index_col=0, parse_dates=True)
d["s"] = d.index.month.map(lambda m: "Winter" if m in (11, 12, 1, 2) else "Sommer" if m in (5, 6, 7, 8) else "Uebergang")
d["p"] = pd.cut(d.index.year, [2017, 2020, 2022, 2023, 2026], labels=["2018-20", "2021-22", "2023", "2024-26"])
g = d.groupby(["p", "s"], observed=True).agg(preis=("mean", "mean"), hl=("hl", "mean")); g["ratio"] = g.hl / g.preis
g.round(2).to_csv("results/season_ratio.csv"); print(g.round(2))
