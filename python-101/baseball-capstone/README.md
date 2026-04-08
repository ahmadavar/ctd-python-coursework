## Baseball Statistics Analysis

#### 📦 Capstone Project Intro

This capstone project focuses on building an end-to-end data pipeline and interactive dashboard to explore historical National League baseball statistics. The project covers the full data workflow — from web scraping and cleaning to database management and interactive visual analytics — providing both technical depth and practical business insights.

#### Streamlit Dashboard Intro

The National League Baseball Dashboard is a lightweight, interactive web application built with Streamlit. It enables users to explore player and team performance trends over time through dynamic charts, filters, and heatmaps, all powered by a local SQLite database containing cleaned historical baseball data.

#### Project Structure
```
CAPSTONE_BASEBALL_SCRAPER_CTD

├── 1.Web_Scraping/                     # Selenium script for scraping baseball data
│   └── selenium_scraper.py
│
├── 2.National_League/                  # Raw National League data files (first result from scraping)
│
├── 3.1.Parsing/                        # Parsing scripts for raw tables
│   └── parse_all_tables.py
│
├── 3.National_League_Cleaned/          # Cleaned CSVs and database creation tools
│   ├── clean_all_nl_v2.py              # Script to clean all National League CSVs
│   ├── clean_nl_csvs.py
│   ├── export_nl_clean_csvs.py         # Optional export script
│   ├── query_nl_db.py                  # SQL query testing tool
│   ├── national_league.db              # Older version of SQLite database (optional/backup)
│   ├── player_hitting_leadersv2.csv    # Cleaned player hitting statistics
│   ├── player_pitching_leadersv2.csv   # Cleaned player pitching statistics
│   ├── team_hitting_leadersv2.csv      # Cleaned team hitting statistics
│   ├── team_pitching_leadersv2.csv     # Cleaned team pitching statistics
│   ├── team_standingsv2.csv            # Cleaned team standings data
│
├── 4.Further_clean_and_EDA/            # Final cleaning and exploratory analysis
│   └── cleaning_eda.py
│
├── 5.Streamlit/                        # Interactive Streamlit dashboard
│   ├── 5.national_league.db            # Final SQLite database for dashboard use
│   └── streamlit_dashboard.py          # Main dashboard application
│
├── create_nl_db.py                     # Master script to load cleaned CSVs into the database
└── README.md                           # Project overview and instructions
```

#### National League Baseball Data Pipeline & Analytics Platform — delivering historical and real-time insights
- Home Run Dominance Across Eras
Players like Ralph Kiner consistently led the National League in home runs during the 1950s, as visualized in the Hitting Leaders tab.

- Pitching Trends Show Evolution of the Game
ERA distributions reveal that pitching performances tightened significantly during certain decades, possibly due to rule changes or pitching strategy evolution.

- Team Performance Heatmap Highlights Historical Giants
Teams like the St. Louis Cardinals and New York Giants show strong performances in wins and batting average across multiple decades.

- Notable Statistical Outliers Detected
Some years display extreme spikes or dips in player or team statistics, which can be easily identified through the interactive charts and heatmaps.

- Era-Specific Dominance by Pitchers
Scatter plots reveal how certain pitchers like Roger Clemens stood out in ERA and strikeouts during their active years.

#### Future Improvements
- Adding West Coast National Leagues to be able seing SF Giants performance
- Enhancing visuals for heatmaps with better scaling for sparse data
- Deployment to Streamlit Cloud for public access(once all bugs troubleshooted).
