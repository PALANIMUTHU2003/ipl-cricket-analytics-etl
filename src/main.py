from transform import transform
from load import save_csv

# from database import create_tables
from database import (
    create_tables,
    insert_dim_teams,
    insert_dim_players,
    insert_dim_venues,
    insert_dim_matches,
    insert_fact_ball_by_ball,
    DB_PATH
)

import sqlite3

def main():
    create_tables()   
    (
        team_records,
        venue_records,
        player_records,
        match_records,
        fact_ball_by_ball
    ) = transform()

    conn = sqlite3.connect(DB_PATH)

    insert_dim_teams(conn, team_records)
    insert_dim_players(conn, player_records)
    insert_dim_venues(conn, venue_records)
    insert_dim_matches(conn, match_records)
    insert_fact_ball_by_ball(conn, fact_ball_by_ball)

    conn.close()

    save_csv(team_records, "dim_teams.csv")
    save_csv(player_records, "dim_players.csv")
    save_csv(venue_records, "dim_venues.csv")
    save_csv(match_records, "dim_matches.csv")
    save_csv(fact_ball_by_ball, "fact_ball_by_ball.csv")


if __name__ == "__main__":
    main()