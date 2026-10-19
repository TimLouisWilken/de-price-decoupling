"""Fetch DE-LU day-ahead prices (Energy-Charts / SMARD, CC BY 4.0) 2018-01-01 .. today."""
import time, json, urllib.request, pandas as pd, datetime as dt
frames = []
for y in range(2018, 2027):
    end = f"{y}-12-31" if y < 2026 else dt.date.today().isoformat()
    url = f"https://api.energy-charts.info/price?bzn=DE-LU&start={y}-01-01&end={end}"
    for k in range(8):
        try:
            d = json.load(urllib.request.urlopen(url, timeout=120)); break
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(20 * (k + 1))
    time.sleep(5)
    s = pd.Series(d["price"], index=pd.to_datetime(d["unix_seconds"], unit="s", utc=True))
    frames.append(s); print(y, len(s))
s = pd.concat(frames); s = s[~s.index.duplicated()].sort_index().dropna()
s.rename("eur_mwh").to_frame().to_csv("data/raw/de_lu_day_ahead.csv")
# NOTE: 2018-01..09 was added from bzn=DE-AT-LU (zone split 2018-10-01), see README.
