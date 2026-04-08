#!/usr/bin/env python
"""
export_nl_clean_csvs.py
-----------------------
Create tidy views in national_league.db and dump them as five
combined CSV files (one per logical table) in National_League_final_data/.
The output mirrors your peer’s American-League files.
"""

import sqlite3, pandas as pd, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)s  %(message)s")

DB_PATH    = "national_league.db"
OUT_DIR    = Path("National_League_final_data")
OUT_DIR.mkdir(exist_ok=True)

VIEWS = {
    # 1 ───────────────────────────────────────────────────────────────
    "nl_player_hitting": """
        SELECT  Year,
                Statistic,
                Name       AS "Name(s)",
                Team       AS "Team(s)",
                `#`,
                NULL       AS "Top 25"
        FROM    player_hitting_leaders
        WHERE   `#` IS NOT NULL
    """,
    # 2 ───────────────────────────────────────────────────────────────
    "nl_player_pitching": """
        SELECT  Year,
                Statistic,
                Name       AS "Name(s)",
                Team       AS "Team(s)",
                `#`,
                NULL       AS "Top 25"
        FROM    player_pitching_leaders
        WHERE   `#` IS NOT NULL
    """,
    # 3 ───────────────────────────────────────────────────────────────
    "nl_team_standings": """
        SELECT  Year,
                Team,
                Wins,
                Losses,
                WP,
                GB,
                Payroll
        FROM    team_standings
    """,
    # 4 ───────────────────────────────────────────────────────────────
    "nl_team_hitting": """
        SELECT  Year,
                Statistic,
                Team       AS "Team(s)",
                `#`
        FROM    team_hitting_leaders
    """,
    # 5 ───────────────────────────────────────────────────────────────
    "nl_team_pitching": """
        SELECT  Year,
                Statistic,
                Team       AS "Team(s)",
                `#`
        FROM    team_pitching_leaders
    """
}

NAME_MAP = {
    "nl_player_hitting":  "1_National_League_Player_Review_Hitting_Statistics_League_Leaders.csv",
    "nl_player_pitching": "2_National_League_Pitcher_Review_Pitching_Statistics_League_Leaders.csv",
    "nl_team_standings":  "3_National_League_Team_Standings.csv",
    "nl_team_hitting":    "4_National_League_Team_Review_Hitting_Statistics_League_Leaderboard.csv",
    "nl_team_pitching":   "5_National_League_Team_Review_Pitching_Statistics_Leaderboard.csv",
}

conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

# ── 1. Create/replace the SQL views ─────────────────────────────────
for view, sql in VIEWS.items():
    cur.execute(f"DROP VIEW IF EXISTS {view};")
    cur.execute(f"CREATE VIEW {view} AS {sql};")
    logging.info("Created view %s", view)

# ── 2. Export each view to a single CSV ─────────────────────────────
for view, csv_name in NAME_MAP.items():
    df = pd.read_sql_query(f"SELECT * FROM {view};", conn)

    # Optional: drop 'Top 25' if it’s all-null
    if "Top 25" in df.columns and df["Top 25"].isna().all():
        df = df.drop(columns=["Top 25"])

    out_path = OUT_DIR / csv_name
    df.to_csv(out_path, index=False)
    logging.info("Wrote %s  (%d rows)", out_path, len(df))

conn.close()
logging.info("🏁 Export complete — files are in %s", OUT_DIR)
