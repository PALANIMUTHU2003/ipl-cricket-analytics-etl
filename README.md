# IPL Cricket Analytics

An end-to-end sports analytics project using IPL ball-by-ball data from Cricsheet.

The project uses Python for data extraction and transformation, SQLite for relational storage, and SQL for cricket-focused analysis. A Power BI dashboard is planned as the next stage of the project.

## Project Overview

This project processes IPL match JSON files and transforms the raw ball-by-ball data into a structured relational data model.

The main goal is to explore:

* Team performance
* Player batting and bowling performance
* Match results
* Venue performance
* Toss and match outcomes
* Season-wise player performance

## Tech Stack

* Python
* Pandas
* JSON
* SQLite
* SQL
* Power BI *(planned)*

## Data Source

The IPL match data is sourced from **Cricsheet**, which provides structured cricket match data in JSON format.

## Project Pipeline

```text
IPL JSON Files
      ↓
Python
      ↓
Extract & Transform
      ↓
Data Cleaning & Standardization
      ↓
Relational Data Model
      ↓
SQLite Database
      ↓
SQL Analysis
      ↓
Power BI Dashboard (Next Stage)
```

## 1. Python ETL

The Python pipeline processes the IPL JSON files and performs the following steps:

* Reads IPL match JSON files
* Extracts teams, players and venues
* Standardizes historical team names
* Standardizes venue names
* Creates IDs for teams, players and venues
* Transforms match-level information
* Transforms ball-by-ball delivery data
* Handles extras and wickets
* Creates relational records for analysis
* Loads the transformed data into SQLite
* Exports transformed tables as CSV files

### Data Standardization

Historical team names are standardized to maintain consistency across seasons.

Examples:

```text
Delhi Daredevils → Delhi Capitals
Kings XI Punjab → Punjab Kings
Royal Challengers Bangalore → Royal Challengers Bengaluru
Rising Pune Supergiants → Rising Pune Supergiant
```

Venue names are also standardized where different names refer to the same venue.

## 2. Data Model

The project uses a simple relational/star-schema-style structure.

### Dimension Tables

#### `dim_teams`

Stores unique IPL teams.

| Column    | Description            |
| --------- | ---------------------- |
| team_id   | Unique team identifier |
| team_name | Team name              |

#### `dim_players`

Stores unique players.

| Column      | Description              |
| ----------- | ------------------------ |
| player_id   | Unique player identifier |
| player_name | Player name              |

#### `dim_venues`

Stores unique venues.

| Column     | Description             |
| ---------- | ----------------------- |
| venue_id   | Unique venue identifier |
| venue_name | Venue name              |

#### `dim_matches`

Stores match-level information.

| Column              | Description                  |
| ------------------- | ---------------------------- |
| match_id            | Match identifier             |
| match_date          | Match date                   |
| season              | IPL season                   |
| match_number        | Match number                 |
| stage               | Tournament stage             |
| overs               | Scheduled overs              |
| balls_per_over      | Balls per over               |
| venue_id            | Venue reference              |
| team1_id            | First team reference         |
| team2_id            | Second team reference        |
| toss_winner_team_id | Toss-winning team            |
| toss_decision       | Bat or field                 |
| winner_team_id      | Match winner                 |
| win_by_runs         | Margin of victory by runs    |
| win_by_wickets      | Margin of victory by wickets |

### Fact Table

#### `fact_ball_by_ball`

Stores delivery-level match data.

| Column          | Description              |
| --------------- | ------------------------ |
| match_id        | Match reference          |
| innings         | Innings number           |
| batting_team_id | Batting team             |
| bowling_team_id | Bowling team             |
| over            | Over number              |
| actual_delivery | Delivery number          |
| batter_id       | Batter reference         |
| bowler_id       | Bowler reference         |
| non_striker_id  | Non-striker reference    |
| batter_runs     | Runs scored by batter    |
| extra_runs      | Runs from extras         |
| extra_type      | Type of extra            |
| total_runs      | Total runs from delivery |
| is_wicket       | Wicket indicator         |
| wicket_kind     | Type of dismissal        |
| player_out_id   | Dismissed player         |

## 3. SQLite Database

The transformed data is loaded into a SQLite database:

```text
ipl_analytics.db
```

The database contains:

```text
dim_teams
dim_players
dim_venues
dim_matches
fact_ball_by_ball
```

The ball-by-ball fact table provides the detailed delivery-level data required for player, team and match analysis.

## 4. SQL Analysis

SQL queries are organized into three levels.

### Basic SQL

The basic analysis covers:

* Total matches
* Total runs
* Total wickets
* Matches by season
* Wins by team

### Intermediate SQL

The intermediate analysis covers:

* Team matches, wins, losses and win percentage
* Player run totals
* Player wicket totals
* Venue performance
* Toss winner vs match winner
* Batting strike rate
* Bowling economy
* Season-wise player performance

### Advanced SQL

The advanced analysis currently includes:

* Top 5 players by runs in each season
* Ranking players within each season using `RANK()`
* Common Table Expressions (CTEs)
* Window functions

Example:

```sql
RANK() OVER (
    PARTITION BY season
    ORDER BY runs DESC
)
```

## 5. Power BI

**Status: In Progress**

The processed IPL dataset will be used to build a Power BI dashboard covering:

* IPL season analysis
* Team performance
* Player performance
* Batting metrics
* Bowling metrics
* Venue performance
* Match results

The Power BI dashboard will be added to this repository once completed.

## Questions Explored

Some of the questions this project aims to answer:

* Which teams have won the most matches?
* Who are the highest run scorers?
* Who has taken the most wickets?
* Which venues have the highest scoring?
* Does winning the toss relate to winning the match?
* Who has the best batting strike rate?
* Which bowlers have the best economy?
* Who are the top players in each season?
* How does player performance change across seasons?

## Project Structure

```text
ipl-cricket-analytics/
│
├── dataset/
│   └── json files/
│
├── output/
│   ├── dim_teams.csv
│   ├── dim_players.csv
│   ├── dim_venues.csv
│   ├── dim_matches.csv
│   └── fact_ball_by_ball.csv
│
├── sql/
│   ├── 01_basic.sql
│   ├── 02_intermediate.sql
│   └── 03_advanced.sql
│
├── src/
│   ├── config.py
│   ├── database.py
│   ├── load.py
│   ├── mappings.py
│   ├── transform.py
│   └── main.py
│
├── ipl_analytics.db
│
└── README.md
```
## Current Status

| Component                       | Status      |
| ------------------------------- | ----------- |
| JSON data extraction            | Completed   |
| Data cleaning & standardization | Completed   |
| Data transformation             | Completed   |
| Relational data modelling       | Completed   |
| SQLite database                 | Completed   |
| CSV export                      | Completed   |
| Basic SQL analysis              | Completed   |
| Intermediate SQL analysis       | Completed   |
| Advanced SQL analysis           | Completed   |
| Power BI dashboard              | In progress |

## Future Improvements

* Complete the Power BI dashboard
* Add more cricket performance metrics
* Add additional analytical queries
* Improve documentation with dashboard screenshots

## Author

**Palanimuthu T**
Data Analyst | Sports Analytics
