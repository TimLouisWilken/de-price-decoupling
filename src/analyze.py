"""Price level vs. volatility (daily high-low spread), DE-LU day-ahead, 2018-2026."""
import pandas as pd, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
s = pd.read_csv("data/raw/de_lu_day_ahead.csv", index_col=0, parse_dates=True).eur_mwh
h = s.tz_convert("Europe/Berlin").resample("1h").mean().dropna()   # 15-min -> hourly (since 2025-10)
day = h.index.tz_localize(None).normalize()
g = h.groupby(day)
d = pd.DataFrame({"mean": g.mean(), "hl": g.max() - g.min(), "n": g.size()})
d = d[d.n >= 23]
d["mean30"], d["hl30"] = d["mean"].rolling(30).mean(), d["hl"].rolling(30).mean()
d["ratio30"] = d.hl30 / d.mean30.clip(lower=20)
d.to_csv("results/daily.csv")
m = d[["mean", "hl"]].resample("MS").mean()
y = d.groupby(d.index.year).apply(lambda x: pd.Series({
    "mean": x["mean"].mean(), "hl": x.hl.mean(), "hl_median": x.hl.median(),
    "corr_daily": x["mean"].corr(x.hl),
    "corr_30d": x.mean30.corr(x.hl30), "days": len(x)}))
y.round(2).to_csv("results/yearly.csv"); print(y.round(2))
# rolling 365d correlation of 30d MAs
d["corr365"] = d.mean30.rolling(365).corr(d.hl30)
fig, ax = plt.subplots(3, 1, figsize=(12, 11), sharex=True)
ax[0].plot(d.mean30, label="Tagesmittel Preis (30d-MA)", color="#1f77b4")
ax[0].plot(d.hl30, label="Hoch-Tief-Spread täglich (30d-MA)", color="#2ca02c")
ax[0].set_ylabel("EUR/MWh"); ax[0].legend(); ax[0].set_title("DE-LU Day-Ahead: Preisniveau vs. Volatilität (Hoch-Tief), 2018–2026")
ax[1].plot(d.corr365, color="k"); ax[1].axhline(0, c="grey", lw=.5); ax[1].set_ylabel("Korrelation (365d, 30d-MAs)")
ax[2].plot(d.ratio30, color="#d62728"); ax[2].set_ylabel("Spread / Preisniveau (30d)")
for a in ax: a.grid(alpha=.3)
# scatter by year
fig, a = plt.subplots(figsize=(8, 6))
sc = a.scatter(m["mean"], m.hl, c=m.index.year + m.index.month / 12, cmap="viridis", s=25)
plt.colorbar(sc, label="Jahr"); a.set_xlabel("Monatsmittel Preis [EUR/MWh]"); a.set_ylabel("Monatsmittel Hoch-Tief-Spread [EUR/MWh]")
print(m.tail(24).round(1))
