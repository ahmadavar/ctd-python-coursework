#!/usr/bin/env python
# tidy_nl_csvs.py  ─ clean all raw National-League CSV tables

from pathlib import Path
import pandas as pd
import csv, re

RAW_DIR  = Path("../2.National_League")          # relative to 3.1.Parsing
TIDY_DIR = Path("../3.National_League_Cleaned")  # output folder
TIDY_DIR.mkdir(exist_ok=True)

table_map = {
    "1": ("player_hitting_leaders.csv",  False),  # drop Top-25 col
    "2": ("player_pitching_leaders.csv", False),
    "3": ("team_standings.csv",          True),   # special parsing
    "4": ("team_hitting_leaders.csv",    True),
    "5": ("team_pitching_leaders.csv",   True),
}
frames = {k: [] for k in table_map}


def _to_int(text: str):
    """Return first integer found in text or None."""
    m = re.search(r"\d+", str(text))
    return int(m.group()) if m else None


for f in RAW_DIR.glob("*_Table_*.csv"):
    year, tbl_no = f.stem.split("_")[0], f.stem.split("_")[2]

    # read whole line as single string; tolerate ragged rows
    df_raw = pd.read_csv(
        f,
        header=None,
        names=["raw"],
        engine="python",
        on_bad_lines="skip",
        skip_blank_lines=True,
    )

    lines = df_raw["raw"].dropna()
    lines = lines[~lines.str.contains("History|→|←", na=False)]

    # ── 3 = team standings ─────────────────────────────────────────
    if tbl_no == "3":
        records = []
        for line in lines.iloc[1:]:          # skip caption
            parts = [p.strip() for p in line.split(",") if p.strip()]
            if len(parts) < 4 or parts[0] == "Payroll":
                continue
            team, wins, losses = parts[0], parts[1], parts[2]
            wp = parts[4] if len(parts) > 4 else None
            gb = parts[5] if len(parts) > 5 else None
            records.append(
                {
                    "Year": int(year),
                    "Team": team,
                    "Wins": _to_int(wins),
                    "Losses": _to_int(losses),
                    "WP": wp,
                    "GB": gb,
                }
            )
        if records:
            frames["3"].append(pd.DataFrame(records))

    # ── leader tables (1,2,4,5) ───────────────────────────────────
    else:
        body = lines.iloc[1:].str.replace("\n", " ", regex=False).tolist()  # ← fix here
        reader = csv.reader(body)

        padded = [(r + [""] * 5)[:5] for r in reader]  # keep every row
        cols = ["Statistic", "Name", "Team", "#", "Top 25"]
        df = pd.DataFrame(padded, columns=cols)
        df.insert(0, "Year", int(year))
        if not table_map[tbl_no][1]:         # drop Top-25 for player tables
            df = df.drop(columns=["Top 25"])
        frames[tbl_no].append(df)

# ── write tidy CSVs ────────────────────────────────────────────────
for tbl_no, (fname, _) in table_map.items():
    if frames[tbl_no]:
        pd.concat(frames[tbl_no], ignore_index=True).to_csv(
            TIDY_DIR / fname, index=False
        )
        print(f"saved {fname}")

print("All tidy CSVs written to", TIDY_DIR)
