#!/usr/bin/env python
"""
query_nl_db.py
--------------
Lightweight command-line client for `national_league.db`.

Features
• Built-in queries:
  • top_players   player stat leaderboard  (JOINs team standings)
  • player_team   season-by-season line for one player incl. team W-L
  • team_summary  year + basic record for one club
• Custom SQL mode:  python query_nl_db.py sql "SELECT …"
• Flags for --year, --stat, --player, --team, --limit
• Graceful error handling + pretty tables
"""

import argparse, sqlite3, sys
import pandas as pd
from pathlib import Path

DB_PATH = Path("national_league.db")   # adjust if you moved the file

# Check if tabulate is installed for pretty printing
try:
    from tabulate import tabulate
    _USE_TABULATE = True
except ImportError:
    _USE_TABULATE = False

def _print_df(df: pd.DataFrame):
    if df.empty:
        print("No rows returned.")
        return
    if _USE_TABULATE:
        print(tabulate(df, headers="keys", tablefmt="simple", showindex=False))
    else:  # fallback
        df.to_csv(sys.stdout, index=False)

#SQL Templates
SQL_TOP_PLAYERS = """
SELECT  p.Year,
        p.Name,
        p.Team,
        p."{stat}"       AS StatValue,
        t.Wins,
        t.Losses
FROM    player_hitting_leaders AS p
LEFT JOIN team_standings  AS t
          ON p.Year = t.Year
         AND p.Team = t.Team
WHERE   p."{stat}" IS NOT NULL
        {year_clause}
ORDER BY StatValue DESC
LIMIT   :limit;
"""

SQL_PLAYER_TEAM = """
SELECT  p.Year,
        p.Team,
        t.Wins,
        t.Losses,
        p.Statistic,
        p."#"           AS Value
FROM    player_hitting_leaders p
LEFT JOIN team_standings t
          ON p.Year = t.Year
         AND p.Team = t.Team
WHERE   p.Name = :player
ORDER BY p.Year;
"""

SQL_TEAM_SUMMARY = """
SELECT Year, Team, Wins, Losses, WP, GB
FROM   team_standings
WHERE  Team LIKE :team
       {year_clause}
ORDER BY Year;
"""

# Main function to parse arguments and run queries
def run():
    if not DB_PATH.exists():
        sys.exit(f"❌ Database {DB_PATH} not found. Run create_nl_db.py first.")

    parser = argparse.ArgumentParser(
        description="Query National-League SQLite database")
    sub = parser.add_subparsers(dest="command", required=True)

    # top_players
    sp = sub.add_parser("top_players",
                        help="Leaderboard for a hitting stat (JOIN with standings)")
    sp.add_argument("--stat", required=True,
                    help='Column name exactly as in CSV header '
                         '(e.g. "Home Runs", "Batting Average")')
    sp.add_argument("--year", type=int, help="Filter by single season")
    sp.add_argument("--limit", type=int, default=10, help="Rows to return (default 10)")

    # player_team
    sp = sub.add_parser("player_team",
                        help="Player’s season lines + team W-L record")
    sp.add_argument("--player", required=True, help='Exact player name in dataset')

    # team_summary
    sp = sub.add_parser("team_summary",
                        help="Basic standings line for one club across seasons")
    sp.add_argument("--team", required=True, help='Team name or substring')
    sp.add_argument("--year", type=int, help="Optional single season filter")

    # raw SQL
    sp = sub.add_parser("sql", help="Run custom SQL passed in quotes")
    sp.add_argument("query", help="SQL string (use double quotes in shell)")

    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)
    try:
        if args.command == "top_players":
            sql = SQL_TOP_PLAYERS.format(
                stat=args.stat,
                year_clause="AND p.Year = :year" if args.year else ""
            )
            df = pd.read_sql_query(sql, conn,
                                   params={"year": args.year, "limit": args.limit})
            _print_df(df)

        elif args.command == "player_team":
            df = pd.read_sql_query(SQL_PLAYER_TEAM, conn,
                                   params={"player": args.player})
            _print_df(df)

        elif args.command == "team_summary":
            sql = SQL_TEAM_SUMMARY.format(
                year_clause="AND Year = :year" if args.year else "")
            df = pd.read_sql_query(sql, conn,
                                   params={"team": f"%{args.team}%",
                                           "year": args.year})
            _print_df(df)

        elif args.command == "sql":
            df = pd.read_sql_query(args.query, conn)
            _print_df(df)

    except sqlite3.Error as e:
        sys.exit(f"SQLite error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run()
