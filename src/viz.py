"""Visualisations (dataviz-skill style: 2 hues, single axis, direct labels, recessive grid)."""
import pandas as pd, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "Helvetica Neue", "axes.edgecolor": GRID, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": .6, "axes.axisbelow": True, "figure.facecolor": "#fcfcfb",
    "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb"})
d = pd.read_csv("results/daily.csv", index_col=0, parse_dates=True)
d["corr365"] = d.mean30.rolling(365).corr(d.hl30)
def title(fig, t, sub): 
    fig.text(.06, .965, t, fontsize=15, weight="bold", color=INK, va="top")
    fig.text(.06, .925, sub, fontsize=10, color=MUTED, va="top")
SRC = "Quelle: Energy-Charts/SMARD (BNetzA, CC BY 4.0), DE-LU Day-Ahead; HL = Tagesmax − Tagesmin der Stundenpreise"

# 1 Overview
fig, ax = plt.subplots(figsize=(12, 6.2)); fig.subplots_adjust(top=.84, bottom=.1, left=.07, right=.9)
ax.axvspan(pd.Timestamp("2021-10-01"), pd.Timestamp("2023-09-30"), color="#000", alpha=.04, lw=0)
ax.axvspan(pd.Timestamp("2023-10-01"), pd.Timestamp("2026-10-31"), color=ORANGE, alpha=.06, lw=0)
ax.plot(d.mean30, color=BLUE, lw=2); ax.plot(d.hl30, color=ORANGE, lw=2)
ax.text(d.index[-1] + pd.Timedelta(days=25), d.mean30.iloc[-1], "Preisniveau\n(Tagesmittel)", color=INK, fontsize=10, va="center")
ax.text(d.index[-1] + pd.Timedelta(days=25), d.hl30.iloc[-1] + 15, "Hoch-Tief-\nSpread", color=INK, fontsize=10, va="center")
ax.text(pd.Timestamp("2022-06-15"), 520, "Gaskrise: Spread folgt Preis", ha="center", color=MUTED, fontsize=9)
ax.text(pd.Timestamp("2025-02-15"), 330, "Abkopplung: Spread > Preis im Frühjahr und Sommer,\nim Winter weiter unter dem Preis", ha="center", color=MUTED, fontsize=9)
ax.set_ylim(0, 540); ax.set_xlim(d.index[0], pd.Timestamp("2026-11-15")); ax.set_ylabel("EUR/MWh (30-Tage-Mittel)")
title(fig, "Die große Abkopplung: Volatilität löst sich vom Preisniveau", "Deutschland, Day-Ahead, 2018 – Okt 2026")
fig.text(.07, .02, SRC, fontsize=8, color=MUTED); fig.savefig("results/figures/01_overview.png", dpi=150)

# 2 Correlation + ratio (two panels, own axes)
fig, ax = plt.subplots(2, 1, figsize=(12, 7.5), sharex=True); fig.subplots_adjust(top=.86, bottom=.07, left=.07, right=.97, hspace=.18)
ax[0].plot(d.corr365, color=INK, lw=2); ax[0].axhline(0, color=MUTED, lw=.8)
ax[0].fill_between(d.index, d.corr365, 0, where=d.corr365 < 0, color=ORANGE, alpha=.35, lw=0)
ax[0].set_ylabel("Korrelation Preis–Spread\n(rollierend 365 Tage)"); ax[0].set_ylim(-.9, 1.05)
ax[0].text(pd.Timestamp("2022-10-01"), .97, "≈ 0,9", ha="center", fontsize=10, color=MUTED)
ax[0].text(pd.Timestamp("2025-10-15"), -.8, "gegenläufig", ha="center", fontsize=10, color=MUTED)
ax[1].plot(d.ratio30, color=ORANGE, lw=2); ax[1].axhline(1, color=MUTED, lw=.8, ls=(0, (4, 3)))
ax[1].text(pd.Timestamp("2018-03-01"), 1.05, "Spread = Preis", fontsize=9, color=MUTED); ax[1].set_ylabel("Spread ÷ Preisniveau\n(30-Tage-Mittel)")
title(fig, "Kopplung gerissen, Spread relativ zum Preis verdoppelt sich", "Oben: Korrelation der 30d-Mittel · Unten: Verhältnis Hoch-Tief-Spread zu Tagesmittelpreis")
fig.text(.07, .01, SRC, fontsize=8, color=MUTED); fig.savefig("results/figures/02_correlation_ratio.png", dpi=150)

# 3 Monthly scatter small multiples by year
m = d[["mean", "hl"]].resample("MS").mean(); m["y"] = m.index.year
yrs = list(range(2018, 2027)); fig, axs = plt.subplots(3, 3, figsize=(11, 10), sharex=True, sharey=True)
fig.subplots_adjust(top=.88, bottom=.07, left=.08, right=.97, hspace=.2, wspace=.08)
for a, y in zip(axs.flat, yrs):
    a.plot([0, 300], [0, 300], color=MUTED, lw=.8, ls=(0, (4, 3)))
    a.scatter(m["mean"], m.hl, s=10, color=GRID, zorder=2)
    s = m[m.y == y]; a.scatter(s["mean"], s.hl, s=42, color=ORANGE if y >= 2024 else BLUE, edgecolor="#fcfcfb", lw=1.5, zorder=3)
    a.set_title(str(y), loc="left", fontsize=11, weight="bold", color=INK); a.set_xlim(0, 300); a.set_ylim(0, 300)
for a in axs[-1]: a.set_xlabel("Ø Preis [EUR/MWh]")
for a in axs[:, 0]: a.set_ylabel("Ø Spread [EUR/MWh]")
title(fig, "Monatswerte: bis 2022 um die Diagonale, ab 2024 klar darüber", "Je Punkt ein Monat · gestrichelt: Spread = Preis · grau: alle anderen Jahre")
fig.text(.08, .01, SRC, fontsize=8, color=MUTED); fig.savefig("results/figures/03_monthly_scatter_by_year.png", dpi=150)

# 4 Heatmaps: monthly mean spread and spread/price by year
cm = LinearSegmentedColormap.from_list("seq", ["#eef3fb", "#2a78d6", "#0e2f5a"])
fig, ax = plt.subplots(1, 2, figsize=(13, 5.5)); fig.subplots_adjust(top=.8, bottom=.12, left=.06, right=.97, wspace=.25)
for a, col, lab in [(ax[0], "hl", "Ø Hoch-Tief-Spread [EUR/MWh]"), (ax[1], "r", "Spread ÷ Preis")]:
    m["r"] = m.hl / m["mean"]; m["mo"] = m.index.month; p = m.pivot(index="y", columns="mo", values=col)
    im = a.imshow(p.values, aspect="auto", cmap=cm); a.grid(False)
    a.set_xticks(range(12)); a.set_xticklabels(list("JFMAMJJASOND")); a.set_yticks(range(len(p))); a.set_yticklabels(p.index)
    for (i, j), v in np.ndenumerate(p.values):
        if not np.isnan(v): a.text(j, i, f"{v:.0f}" if col == "hl" else f"{v:.1f}", ha="center", va="center", fontsize=7.5,
                                   color="white" if im.norm(v) > .5 else INK)
    a.set_title(lab, loc="left", fontsize=10, color=INK)
title(fig, "Seit 2024 liegt der Spread auch relativ zum Preis dauerhaft hoch – am stärksten im Frühjahr/Sommer", "Monat × Jahr, Deutschland Day-Ahead")
fig.text(.06, .01, SRC, fontsize=8, color=MUTED); fig.savefig("results/figures/04_seasonality_heatmap.png", dpi=150)

# 5 Hourly shape by year (cause)
s = pd.read_csv("data/raw/de_lu_day_ahead.csv", index_col=0, parse_dates=True).eur_mwh
h = s.tz_convert("Europe/Berlin").resample("1h").mean().dropna(); h.index = h.index.tz_localize(None)
fig, axs = plt.subplots(1, 2, figsize=(12, 5.2), sharey=True); fig.subplots_adjust(top=.82, bottom=.16, left=.07, right=.97, wspace=.06)
for a, mon, nm in [(axs[0], [11, 12, 1, 2], "Winter (Nov–Feb)"), (axs[1], [5, 6, 7, 8], "Sommer (Mai–Aug)")]:
    for y, c, lw in [(2019, "#b9c6d8", 1.5), (2021, "#8fb1de", 1.5), (2023, BLUE, 2), (2025, ORANGE, 2.4)]:
        x = h[(h.index.year == y) & h.index.month.isin(mon)]; pr = x.groupby(x.index.hour).mean()
        a.plot(pr.index, pr.values, color=c, lw=lw); a.text(23.2, pr.values[-1] + {2023: 7, 2025: -7}.get(y, 0) if mon[0] == 5 else pr.values[-1], str(y), color=INK, fontsize=9, va="center")
    a.set_title(nm, loc="left", fontsize=11, weight="bold", color=INK); a.set_xlim(0, 23.8); a.set_xticks([0,6,12,18,23]); a.set_xlabel("Stunde (Berlin)")
axs[0].set_ylabel("Ø Preis [EUR/MWh]")
title(fig, "Ursache: Mittagstal und Abendspitze", "Mittleres Tagesprofil nach Jahr – Spread entsteht zwischen Solar-Mittag und gasgesetzter Abendrampe")
fig.text(.07, .01, SRC, fontsize=8, color=MUTED); fig.savefig("results/figures/05_hourly_profile.png", dpi=150)
