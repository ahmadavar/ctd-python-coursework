import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="National League Baseball Dashboard",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Database Connection ---
DB_PATH = "5.national_league.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

@st.cache_data
def run_query(query):
    try:
        conn = get_connection()
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame()

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Get available years
@st.cache_data
def get_years():
    query = "SELECT DISTINCT Year FROM player_hitting_leaders ORDER BY Year"
    df = run_query(query)
    return df['Year'].tolist() if not df.empty else list(range(1901, 2022))

years = get_years()
min_year = min(years) if years else 1901
max_year = max(years) if years else 2022

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, min_year + 20)
)

# Get Hitting and Pitching Statistics
@st.cache_data
def get_stats(table):
    query = f"SELECT DISTINCT Statistic FROM {table} ORDER BY Statistic"
    df = run_query(query)
    return df['Statistic'].tolist() if not df.empty else []

hitting_stats = get_stats("player_hitting_leaders")
pitching_stats = get_stats("player_pitching_leaders")

# --- Dashboard Tabs ---
tab1, tab2, tab3 = st.tabs(["Hitting Leaders", "Pitching Performance", "Team Analysis"])

# --- Tab 1: Hitting Leaders ---
with tab1:
    st.header("Hitting Leaders (National League)")

    selected_hitting_stat = st.selectbox("Select Hitting Statistic", hitting_stats)

    query = f"""
    SELECT Year, Name, Team, "#" as Value
    FROM player_hitting_leaders
    WHERE Statistic = '{selected_hitting_stat}'
    AND Year BETWEEN {year_range[0]} AND {year_range[1]}
    ORDER BY Year, Value DESC
    """
    df = run_query(query)

    if not df.empty:
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

        top_n = st.slider("Top Players per Year", 1, 10, 3)
        top_df = df.groupby("Year").head(top_n)

        fig1 = px.line(
            top_df, x="Year", y="Value", color="Name",
            title=f"Top {top_n} {selected_hitting_stat} Leaders Over Time",
            markers=True
        )
        st.plotly_chart(fig1, use_container_width=True)

        specific_year = st.selectbox("Select Year to View Leaders", sorted(df['Year'].unique()))
        year_df = df[df['Year'] == specific_year].head(10)

        fig2 = px.bar(
            year_df, x="Name", y="Value", color="Team",
            title=f"Top {selected_hitting_stat} Leaders in {specific_year}"
        )
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

# --- Tab 2: Pitching Performance ---
with tab2:
    st.header("Pitching Performance (National League)")

    selected_pitching_stat = st.selectbox("Select Pitching Statistic", pitching_stats)

    query = f"""
    SELECT Year, Name, Team, "#" as Value
    FROM player_pitching_leaders
    WHERE Statistic = '{selected_pitching_stat}'
    AND Year BETWEEN {year_range[0]} AND {year_range[1]}
    ORDER BY Year, Value
    """
    df = run_query(query)

    if not df.empty:
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

        top_n = st.slider("Top Pitchers per Year", 1, 10, 3)

        if selected_pitching_stat == "ERA":
            df = df.sort_values(["Year", "Value"], ascending=[True, True])
        else:
            df = df.sort_values(["Year", "Value"], ascending=[True, False])

        top_df = df.groupby("Year").head(top_n)

        fig3 = px.scatter(
            top_df, x="Year", y="Value", color="Name", size="Value",
            trendline="lowess",
            title=f"Top {top_n} {selected_pitching_stat} Leaders Over Time"
        )
        st.plotly_chart(fig3, use_container_width=True)

        fig4 = px.box(
            df, x="Year", y="Value",
            title=f"Distribution of {selected_pitching_stat} by Year"
        )
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("No pitching data available for the selected filters.")

# --- Tab 3: Team Analysis ---
with tab3:
    st.header("Team Performance (National League)")

    team_stats = ["Batting Average", "Home Runs", "ERA", "Wins"]
    selected_team_stat = st.selectbox("Select Team Statistic", team_stats)

    if selected_team_stat in ["Batting Average", "Home Runs"]:
        table = "team_hitting_leaders"
    else:
        table = "team_pitching_leaders"

    query = f"""
    SELECT Year, Team, "#" as Value, Statistic
    FROM {table}
    WHERE Statistic = '{selected_team_stat}'
    AND Year BETWEEN {year_range[0]} AND {year_range[1]}
    ORDER BY Year, Value DESC
    """
    df = run_query(query)

    if not df.empty:
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

        pivot = df.pivot(index="Team", columns="Year", values="Value").fillna(0)

        color_scale = 'RdYlGn_r' if selected_team_stat == "ERA" else 'RdYlGn'

        fig5 = px.imshow(
            pivot,
            labels=dict(x="Year", y="Team", color=selected_team_stat),
            color_continuous_scale=color_scale,
            title=f"Team {selected_team_stat} Performance Heatmap"
        )
        st.plotly_chart(fig5, use_container_width=True)

        teams = st.multiselect("Compare Teams", sorted(df['Team'].unique()))

        if teams:
            compare_df = df[df['Team'].isin(teams)]
            fig6 = px.line(
                compare_df, x="Year", y="Value", color="Team", markers=True,
                title=f"{selected_team_stat} Trends for Selected Teams"
            )
            st.plotly_chart(fig6, use_container_width=True)
    else:
        st.warning("No team data available for the selected filters.")

# --- Footer ---
st.markdown("---")
st.caption("© 2025 National League Baseball Dashboard | Built with Streamlit")
