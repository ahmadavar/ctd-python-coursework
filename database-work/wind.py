import plotly.express as px
import plotly.data as pldata
import pandas as pd

# 1. Loading wind dataset
df = pldata.wind(return_type='pandas')

# 2. First and last 10 rows
print("First 10 rows:\n", df.head(10))
print("\nLast 10 rows:\n", df.tail(10))

# 3. Clean the 'strength' column

df['strength'] = df['strength'].str.replace('[^\d.]', '', regex=True).astype(float)

# 4. Create the scatter plot
fig = px.scatter(
    df,
    x='strength',
    y='frequency',
    color='direction',
    title='Wind Strength vs. Frequency by Direction',
    labels={'strength': 'Wind Strength', 'frequency': 'Frequency'}
)

# 5. Save to HTML
fig.write_html("wind.html")

print("Plot saved to wind.html and available to be opened in browser")
