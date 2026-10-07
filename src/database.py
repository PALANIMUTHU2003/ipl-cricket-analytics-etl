import sqlite3

from config import BASE_DIR

DB_PATH = BASE_DIR / "ipl_analytics.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_teams (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_players (
            player_id INTEGER PRIMARY KEY,
            player_name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_venues (
            venue_id INTEGER PRIMARY KEY,
            venue_name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_matches (
            match_id INTEGER PRIMARY KEY,
            match_date TEXT,
            season TEXT,
            match_number INTEGER,
            stage TEXT,
            overs INTEGER,
            balls_per_over INTEGER,
            venue_id INTEGER,
            team1_id INTEGER,
            team2_id INTEGER,
            toss_winner_team_id INTEGER,
            toss_decision TEXT,
            winner_team_id INTEGER,
            win_by_runs INTEGER,
            win_by_wickets INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_ball_by_ball (
            match_id INTEGER,
            innings INTEGER,
            batting_team_id INTEGER,
            bowling_team_id INTEGER,
            over INTEGER,
            actual_delivery INTEGER,
            batter_id INTEGER,
            bowler_id INTEGER,
            non_striker_id INTEGER,
            batter_runs INTEGER,
            extra_runs INTEGER,
            extra_type TEXT,
            total_runs INTEGER,
            is_wicket INTEGER,
            wicket_kind TEXT,
            player_out_id INTEGER
        )
    """)


    conn.commit()
    conn.close()

def insert_dim_teams(conn, team_records):

    cursor = conn.cursor()

    cursor.executemany(
        """
        INSERT INTO dim_teams(team_id, team_name)
        VALUES (?, ?)
        """,
        [
            (team["team_id"], team["team_name"])
            for team in team_records
        ]
    )

    conn.commit()

def insert_dim_players(conn, player_records):

    cursor = conn.cursor()

    cursor.executemany(
        """
        INSERT INTO dim_players (
            player_id,
            player_name
        )
        VALUES (?, ?)
        """,
        [
            (
                player["player_id"],
                player["player_name"]
            )
            for player in player_records
        ]
    )

    conn.commit()

def insert_dim_venues(conn, venue_records):

    cursor = conn.cursor()

    cursor.executemany(
        """
        INSERT INTO dim_venues (
            venue_id,
            venue_name
        )
        VALUES (?, ?)
        """,
        [
            (
                venue["venue_id"],
                venue["venue_name"]
            )
            for venue in venue_records
        ]
    )

    conn.commit()

def insert_dim_matches(conn, match_records):

    cursor = conn.cursor()

    cursor.executemany(
        """
        INSERT INTO dim_matches (
            match_id,
            match_date,
            season,
            match_number,
            stage,
            overs,
            balls_per_over,
            venue_id,
            team1_id,
            team2_id,
            toss_winner_team_id,
            toss_decision,
            winner_team_id,
            win_by_runs,
            win_by_wickets
        )
        VALUES (
            :match_id,
            :match_date,
            :season,
            :match_number,
            :stage,
            :overs,
            :balls_per_over,
            :venue_id,
            :team1_id,
            :team2_id,
            :toss_winner_team_id,
            :toss_decision,
            :winner_team_id,
            :win_by_runs,
            :win_by_wickets
        )
        """,
        match_records
    )

    conn.commit()

def insert_fact_ball_by_ball(conn, fact_ball_by_ball):

    cursor = conn.cursor()

    cursor.executemany(
        """
        INSERT INTO fact_ball_by_ball (
            match_id,
            innings,
            batting_team_id,
            bowling_team_id,
            over,
            actual_delivery,
            batter_id,
            bowler_id,
            non_striker_id,
            batter_runs,
            extra_runs,
            extra_type,
            total_runs,
            is_wicket,
            wicket_kind,
            player_out_id
        )
        VALUES (
            :match_id,
            :innings,
            :batting_team_id,
            :bowling_team_id,
            :over,
            :actual_delivery,
            :batter_id,
            :bowler_id,
            :non_striker_id,
            :batter_runs,
            :extra_runs,
            :extra_type,
            :total_runs,
            :is_wicket,
            :wicket_kind,
            :player_out_id
        )
        """,
        fact_ball_by_ball
    )

    conn.commit()


