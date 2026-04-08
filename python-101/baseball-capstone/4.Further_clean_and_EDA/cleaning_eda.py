import pandas as pd
import numpy as np
import re

# File paths for v2
files = {
    "player_hitting": "../3.National_League_Cleaned/player_hitting_leadersv2.csv",
    "player_pitching": "../3.National_League_Cleaned/player_pitching_leadersv2.csv",
    "team_hitting": "../3.National_League_Cleaned/team_hitting_leadersv2.csv",
    "team_pitching": "../3.National_League_Cleaned/team_pitching_leadersv2s.csv",
    "team_standings": "../3.National_League_Cleaned/team_standingsv2.csv"
}

# Function to clean problematic numeric columns with commas, symbols, etc.
def clean_numeric_column(df, col="#"):
    df_copy = df.copy()

    def convert(val):
        if pd.isna(val):
            return np.nan
        str_val = str(val).replace(",", "").strip()
        match = re.search(r"(\d+\.?\d*)", str_val)
        return float(match.group(1)) if match else np.nan

    df_copy[col] = df_copy[col].apply(convert)
    nan_count = df_copy[col].isna().sum()
    print(f"NaN count in '{col}' after conversion: {nan_count}")

    df_copy[col] = df_copy[col].round(3)
    return df_copy

# Load and process Player Hitting
df_ph = pd.read_csv(files["player_hitting"])
print("\n=== Player Hitting Data Types ===")
print(df_ph.dtypes)
print(df_ph.head())

# Load and process Player Pitching
df_pp = pd.read_csv(files["player_pitching"])
print("\n=== Player Pitching Data Types Before Cleaning ===")
print(df_pp.dtypes)
print(df_pp.head())

df_pp_clean = clean_numeric_column(df_pp)
df_pp_clean.to_csv(files["player_pitching"], index=False)
print(f"✅ Cleaned and saved: {files['player_pitching']}")

# Load and process Team Hitting
df_th = pd.read_csv(files["team_hitting"])
print("\n=== Team Hitting Data Types Before Cleaning ===")
print(df_th.dtypes)
print(df_th.head())

df_th_clean = clean_numeric_column(df_th)
df_th_clean.to_csv(files["team_hitting"], index=False)
print(f"✅ Cleaned and saved: {files['team_hitting']}")

# Load and process Team Pitching
df_tp = pd.read_csv(files["team_pitching"])
print("\n=== Team Pitching Data Types Before Cleaning ===")
print(df_tp.dtypes)
print(df_tp.head())

df_tp_clean = clean_numeric_column(df_tp)
df_tp_clean.to_csv(files["team_pitching"], index=False)
print(f"✅ Cleaned and saved: {files['team_pitching']}")

# Load and process Team Standings
df_ts = pd.read_csv(files["team_standings"])
print("\n=== Team Standings Sample ===")
print(df_ts.dtypes)
print(df_ts.head())

print("\n✅ Team Standings reviewed - no '#' column expected here, so no numeric cleaning applied.")
