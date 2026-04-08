#!/usr/bin/env python
"""
clean_all_nl.py — tidy every National-League CSV table into 5 files
• Reads ../2.National_League/*_Table_*.csv
• Writes ../3.National_League_Cleaned/
      ├─ player_hitting_leaders.csv
      ├─ player_pitching_leaders.csv
      ├─ team_standings.csv
      ├─ team_hitting_leaders.csv
      └─ team_pitching_leaders.csv
"""

from pathlib import Path
import pandas as pd
import re, csv, logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

RAW_DIR   = Path("../2.National_League")          # raw single-season files
CLEAN_DIR = Path("../3.National_League_Cleaned")  # output folder
CLEAN_DIR.mkdir(exist_ok=True)

OUT = {
    "1": {"file": "player_hitting_leadersv2.csv",
          "cols": ["Year","Statistic","Name","Team","#"] , "rows": []},
    "2": {"file": "player_pitching_leadersv2.csv",
          "cols": ["Year","Statistic","Name","Team","#"] , "rows": []},
    "3": {"file": "team_standingsv2.csv",
          "cols": ["Year","Team","Wins","Losses","Ties","WP","GB","Payroll"],
          "rows": []},
    "4": {"file": "team_hitting_leadersv2.csv",
          "cols": ["Year","Statistic","Team","#"] , "rows": []},
    "5": {"file": "team_pitching_leadersv2s.csv",
          "cols": ["Year","Statistic","Team","#"] , "rows": []},
}

int_pat = re.compile(r"\d+")

def to_int(text):
    m = int_pat.search(str(text))
    return int(m.group()) if m else None

for path in RAW_DIR.glob("*_Table_*.csv"):
    year, tbl = path.stem.split("_")[0], path.stem.split("_")[2]
    logging.info("Processing %s", path.name)

    # read each line as raw text, keep non-blank rows
    lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    # drop obvious junk/captions
    lines = [l for l in lines if not re.search("History|→|←", l)]

    if tbl == "3":                                  # ── standings table
        for row in lines[1:]:                       # skip caption row
            parts = [p.strip() for p in row.split(",") if p.strip()]
            if len(parts) < 4 or parts[0] == "Payroll":
                continue
            record = {
                "Year": int(year),
                "Team":   parts[0],
                "Wins":   to_int(parts[1]),
                "Losses": to_int(parts[2]),
                "Ties":   to_int(parts[3]) if len(parts) > 3 else None,
                "WP":     parts[4] if len(parts) > 4 else None,
                "GB":     parts[5] if len(parts) > 5 else None,
                "Payroll":parts[6] if len(parts) > 6 else None,
            }
            OUT["3"]["rows"].append(record)

    else:                                           # ── leader tables
        body = [l.replace("\n"," ").strip() for l in lines[1:]]  # drop caption
        reader = csv.reader(body)
        for r in reader:
            if len(r) < 2 or r[0] == "Statistic":
                continue
            r += [""] * 5               # pad to at least 5 elements
            if tbl in ("1","2"):        # remove Top-25 column
                r = r[:4] + [r[3]]      # keep first 4 (Statistic Name Team #)
            record = {"Year": int(year)}
            record.update(dict(zip(OUT[tbl]["cols"][1:], r[:len(OUT[tbl]["cols"])-1])))
            OUT[tbl]["rows"].append(record)

# ── write tidy master files ────────────────────────────────────────
for meta in OUT.values():
    df = pd.DataFrame(meta["rows"], columns=meta["cols"])
    df.to_csv(CLEAN_DIR / meta["file"], index=False)
    logging.info("Saved %s (%d rows)", meta["file"], len(df))

logging.info("All five tidy CSVs are in %s", CLEAN_DIR.resolve())
