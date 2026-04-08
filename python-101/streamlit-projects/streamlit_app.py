import streamlit as st
import pandas as pd
import plotly.express as px

# Title and description
st.title("Sales Performance Dashboard")
st.markdown("""
This dashboard helps explore sales and order performance using transactional and customer data.
""")

# Load CSVs with correct paths
base_path = "../db/csv/"

customers = pd.read_csv(base_path + "customers.csv")
employees = pd.read_csv(base_path + "employees.csv")
orders = pd.read_csv(base_path + "orders.csv")
line_items = pd.read_csv(base_path + "line_items.csv")
products = pd.read_csv(base_path + "products.csv")

# Cleaning summary
st.markdown("### Data Cleaning Summary")
st.markdown("""
- Ensured valid foreign keys between tables
- Joined tables to create full order-level view
- Converted dates to datetime objects
""")

# Merge datasets into one master DataFrame
orders['date'] = pd.to_datetime(orders['date'])

df = (line_items
      .merge(orders, on='order_id')
      .merge(products, on='product_id')
      .merge(employees, on='employee_id'))

df['total_price'] = df['price'] * df['quantity']

# Show merged dataset
st.subheader("Merged Sales Data")
st.dataframe(df.head())

# Plot 1: Revenue over time
st.markdown("### Revenue Over Time")
revenue_by_day = df.groupby(df['date'].dt.date)['total_price'].sum().reset_index()
fig1 = px.line(revenue_by_day, x='date', y='total_price',
               labels={'date': 'Order Date', 'total_price': 'Revenue'},
               title='Daily Revenue')
st.plotly_chart(fig1)

# Plot 2: Average order value by employee
st.markdown("### Average Order Value by Employee")
df_emp = df.groupby(['employee_id', 'first_name', 'last_name'])['total_price'].mean().reset_index()
df_emp['employee'] = df_emp['first_name'] + ' ' + df_emp['last_name']
fig2 = px.bar(df_emp, x='employee', y='total_price',
              labels={'employee': 'Employee', 'total_price': 'Avg Order Value'},
              title='Average Order Value by Employee')
st.plotly_chart(fig2)
