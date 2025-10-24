# tidy_data.py  (place in project ROOT, not in /data)
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

RIDERSHIP_IN  = DATA / "ridership_headline.csv"          # downloaded original
RIDERSHIP_OUT = DATA / "ridership_daily.csv"             # filtered output

POP_IN  = DATA / "population_district.csv"               # downloaded original
POP_OUT = DATA / "population_district_2024_kl_sgr.csv"   # filtered output

# --- 1) Ridership: keep KL services + date, optionally last N months ---
use_cols = [
    "date",
    "rail_mrt_kajang",
    "rail_mrt_pjy",
    "rail_lrt_kj",
    "rail_lrt_ampang",
    "rail_monorail",
    "bus_rkl",
]

print(f"Reading: {RIDERSHIP_IN}")
df = pd.read_csv(RIDERSHIP_IN, parse_dates=["date"])
df = df[[c for c in use_cols if c in df.columns]].copy()

# OPTIONAL: keep last N months (set to 24; change to 12 if you want)
N_MONTHS = 24
cutoff = df["date"].max() - pd.DateOffset(months=N_MONTHS)
df = df[df["date"] >= cutoff].sort_values("date")

df.to_csv(RIDERSHIP_OUT, index=False)
print(f"Wrote: {RIDERSHIP_OUT}  ({len(df)} rows, {len(df.columns)} cols)")

# --- 2) Population: filter KL & Selangor for year 2024 only ---
print(f"Reading: {POP_IN}")
pop = pd.read_csv(POP_IN, parse_dates=["date"])

mask_state = pop["state"].isin(["Kuala Lumpur", "Selangor"])
mask_year  = pop["date"] == pd.Timestamp("2024-01-01")

keep_cols = [c for c in ["state", "district", "population"] if c in pop.columns]
pop_out = pop.loc[mask_state & mask_year, keep_cols].copy()

pop_out.to_csv(POP_OUT, index=False)
print(f"Wrote: {POP_OUT}  ({len(pop_out)} rows, {len(pop_out.columns)} cols)")
