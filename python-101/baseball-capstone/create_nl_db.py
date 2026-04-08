import sqlite3
import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)s  %(message)s")

# Correct folder and DB path for your project
CLEAN_DIR = Path("3.National_League_Cleaned")
DB_PATH = "5.national_league.db"

if not CLEAN_DIR.exists():
    logging.error("Folder %s not found. Check your folder path.", CLEAN_DIR)
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
logging.info("Opened SQLite DB: %s", DB_PATH)

for csv_file in CLEAN_DIR.glob("*v2*.csv"):
    # Remove 'v2' from table name to match Streamlit expectations
    table_name = csv_file.stem.replace("v2", "")
    logging.info("Importing %s → table %s", csv_file.name, table_name)

    try:
        df = pd.read_csv(csv_file)

        # Build dtype map for proper storage
        dtype_map = {
            col: "INTEGER" for col in df.columns if df[col].dtype.kind in "iu"
        }
        dtype_map.update({
            col: "REAL" for col in df.columns if df[col].dtype.kind == "f"
        })

        df.to_sql(table_name, conn, if_exists="replace", index=False, dtype=dtype_map)
        logging.info("✓ %s rows imported into %s", len(df), table_name)

    except Exception as e:
        logging.error("🚨 Failed on %s: %s", csv_file.name, e)

conn.close()
logging.info("All tables loaded. You can now query %s", DB_PATH)
