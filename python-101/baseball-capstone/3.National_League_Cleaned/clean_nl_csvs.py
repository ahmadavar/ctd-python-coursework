"""
Cleaning every raw National-League CSV produced by the scraper.

• Adding a Year column derived from the filename
• Stripping duplicate caption rows
• Converting numeric strings ("1,544"  ".362" "—") → int/float/NaN
• Saving results in National_League_clean_data/ with clear table names
"""

import pandas as pd
from pandas.api.types import is_string_dtype
import glob
import os
import re
import logging
import numpy as np
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)s  %(message)s")

RAW_DIR = Path("National_League")
CLEAN_DIR = Path("National_League_Cleaned")  # new folder
CLEAN_DIR.mkdir(exist_ok=True)

# Map table-number → logical name
TABLE_MAP = {
    "1": "player_hitting_leaders",
    "2": "player_pitching_leaders",
    "3": "team_standings",
    "4": "team_hitting_leaders",
    "5": "team_pitching_leaders",
}


def tidy_numeric(series: pd.Series):
    """
    Strip commas / percent signs / stray text
    and return a float column.  Anything that still
    doesn't look numeric becomes NaN (errors='coerce').
    """
    cleaned = (
        series.astype(str)
              .str.replace("[^0-9.+-]", "", regex=True)  # keep digits . + -
              .str.replace(",", "", regex=False)
              .str.strip()
              .replace({"": np.nan, "-": np.nan, "—": np.nan})
    )
    return pd.to_numeric(cleaned, errors="coerce")

for csv_path in glob.glob(str(RAW_DIR / "*.csv")):
    year, tbl_no = re.search(r"(\d{4})_Table_(\d+)\.csv", csv_path).groups()
    logical_name = TABLE_MAP.get(tbl_no, f"table_{tbl_no}")

    df = pd.read_csv(csv_path)

    # 1. Drop rows that exactly duplicate header or contain only NaN
    df = df.dropna(how="all")
    df = df[~df.eq(df.columns).all(axis=1)]

    # 2. Add Year column
    df.insert(0, "Year", int(year))

    # 3. Coerce obvious numeric fields
    for col in df.columns:
        # ── A. Skip columns that are already numeric ───────────────────────────
        if not is_string_dtype(df[col]):
            continue

        # ── B. Convert columns that *look* numeric ────────────────────────────
        if (
            col.lower()
            in {
                "wins",
                "losses",
                "gb",
                "#",
                "payroll",
                "rbi",
                "home runs",
                "doubles",
                "triples",
                "runs",
            }
            or df[col].str.contains(r"\d").any()  # any cell contains a digit
        ):
            df[col] = tidy_numeric(df[col])

    # 4. Write cleaned file
    out_path = CLEAN_DIR / f"{logical_name}.csv"
    mode = "a" if out_path.exists() else "w"
    header = not out_path.exists()
    df.to_csv(out_path, mode=mode, header=header, index=False)
    logging.info(f"Appended {len(df)} rows → {out_path}")

logging.info("Cleaning phase complete.")
