import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Step 1: Connect to the database and run the SQL query
conn = sqlite3.connect('db/lesson.db')

query = """
SELECT o.order_id,
       SUM(p.price * l.quantity) AS total_price
FROM orders o
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id;
"""

df = pd.read_sql_query(query, conn)
conn.close()

# Option A(more manual): Using apply (more manual)
# def cumulative(row):
#     totals_above = df['total_price'][0:row.name+1]
#     return totals_above.sum()
# df['cumulative'] = df.apply(cumulative, axis=1)

# Alternative faster option: Easier and faster using cumsum
df['cumulative'] = df['total_price'].cumsum()

# Step 3: Plot cumulative revenue vs. order_id
df.plot(kind='line', x='order_id', y='cumulative', title='Cumulative Revenue Over Orders', color='green')

# Label the axes and plotting
plt.xlabel('Order ID')
plt.ylabel('Cumulative Revenue ($)')
plt.grid(True)
plt.tight_layout()
plt.show()
