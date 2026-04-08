import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database located one level up
conn = sqlite3.connect('db/lesson.db')

# SQL query to calculate revenue by employee
query = """
SELECT last_name,
       SUM(price * quantity) AS revenue
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY e.employee_id;
"""

# Read SQL result into DataFrame
employee_results = pd.read_sql_query(query, conn)

# Close the DB connection
conn.close()

# Plotting the bar chart using Pandas
employee_results.plot(
    kind='bar',
    x='last_name',
    y='revenue',
    color='skyblue',
    title='Revenue by Employee'
)

# Labeling
plt.xlabel('Employee Last Name')
plt.ylabel('Total Revenue ($)')
plt.tight_layout()

# Show plot
plt.show()
