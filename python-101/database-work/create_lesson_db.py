import pandas as pd
import sqlite3
import os
# Path to your CSV files
base_path = './db/csv'

# Load CSVs into DataFrames
employees_df = pd.read_csv(os.path.join(base_path, 'employees.csv'))
orders_df = pd.read_csv(os.path.join(base_path, 'orders.csv'))
products_df = pd.read_csv(os.path.join(base_path, 'products.csv'))
line_items_df = pd.read_csv(os.path.join(base_path, 'line_items.csv'))  # if available

# Create SQLite database under db/
conn = sqlite3.connect('./db/lesson.db')

# Save tables
employees_df.to_sql('employees', conn, if_exists='replace', index=False)
orders_df.to_sql('orders', conn, if_exists='replace', index=False)
products_df.to_sql('products', conn, if_exists='replace', index=False)
line_items_df.to_sql('line_items', conn, if_exists='replace', index=False)

conn.close()

print(" lesson.db created successfully.")
