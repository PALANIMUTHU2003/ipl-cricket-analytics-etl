import json

from config import json_files
from mappings import team_name_mapping, venue_name_mapping

def transform():

    # DIM_TEAMS
    teams = set()

    for json_file in json_files:

        with open(json_file, "r", encoding="utf-8") as file:
            match_data = json.load(file)

        info = match_data["info"]

        team1 = team_name_mapping.get(
            info["teams"][0],
            info["teams"][0]
        )

        team2 = team_name_mapping.get(
            info["teams"][1],
            info["teams"][1]
        )

        teams.add(team1)
        teams.add(team2)

    # print(f"Total Teams : {len(teams)}")


    team_records = []

    for team in sorted(teams):

        team_records.append({
            "team_id": len(team_records) + 1,
            "team_name": team
        })


    team_lookup = {}

    for team in team_records:
        team_lookup[team["team_name"]] = team["team_id"]

    # print(team_records)
    # print(team_lookup)


    # DIM_VENUES
    venues = set()

    for json_file in json_files:

        with open(json_file, "r", encoding="utf-8") as file:
            match_data = json.load(file)

        info = match_data["info"]

        venue_name = venue_name_mapping.get(
            info["venue"],
            info["venue"]
        )

        venues.add(venue_name)

    # print(f"Total Venues : {len(venues)}")


    venue_records = []

    for venue in sorted(venues):

        venue_records.append({
            "venue_id": len(venue_records) + 1,
            "venue_name": venue
        })


    venue_lookup = {}

    for venue in venue_records:
        venue_lookup[venue["venue_name"]] = venue["venue_id"]

    # print(venue_records)
    # print(venue_lookup)

    # DIM_PLAYERS
    players = set()

    for json_file in json_files:

        with open(json_file, "r", encoding="utf-8") as file:
            match_data = json.load(file)

        info = match_data["info"]

        for team in info["players"]:
            for player in info["players"][team]:
                players.add(player)

    # print(f"Total Players : {len(players)}")


    player_records = []

    for player in sorted(players):

        player_records.append({
            "player_id": len(player_records) + 1,
            "player_name": player
        })


    player_lookup = {}

    for player in player_records:
        player_lookup[player["player_name"]] = player["player_id"]

    # print(player_records)
    # print(player_lookup)

    # FACT_BALL_BY_BALL
    fact_ball_by_ball = []

    for json_file in json_files:

        with open(json_file, "r", encoding="utf-8") as file:
            match_data = json.load(file)

        info = match_data["info"]
        match_id = json_file.stem

        # Match Teams
        team1 = team_name_mapping.get(
            info["teams"][0],
            info["teams"][0]
        )

        team2 = team_name_mapping.get(
            info["teams"][1],
            info["teams"][1]
        )

        team1_id = team_lookup[team1]
        team2_id = team_lookup[team2]

        # Innings
        for innings_number, innings in enumerate(match_data["innings"], start=1):

            batting_team = team_name_mapping.get(
                innings["team"],
                innings["team"]
            )

            batting_team_id = team_lookup[batting_team]

            bowling_team_id = (
                team2_id if batting_team_id == team1_id
                else team1_id
            )

            # Overs
            for over in innings["overs"]:

                over_number = over["over"]

                # Deliveries
                for delivery in over["deliveries"]:

                    batter_id = player_lookup[delivery["batter"]]
                    bowler_id = player_lookup[delivery["bowler"]]
                    non_striker_id = player_lookup[delivery["non_striker"]]

                    batter_runs = delivery["runs"]["batter"]
                    extra_runs = delivery["runs"]["extras"]
                    total_runs = delivery["runs"]["total"]

                    # Extras
                    extra_type = None
                    if "extras" in delivery:
                        extra_type = list(delivery["extras"].keys())[0]

                    # Wicket
                    is_wicket = 0
                    wicket_kind = None
                    player_out_id = None

                    if "wickets" in delivery:

                        wicket = delivery["wickets"][0]

                        is_wicket = 1
                        wicket_kind = wicket["kind"]
                        player_out_id = player_lookup[wicket["player_out"]]

                    fact_ball_by_ball.append({

                        "match_id": match_id,

                        "innings": innings_number,

                        "batting_team_id": batting_team_id,
                        "bowling_team_id": bowling_team_id,

                        "over": over_number,
                        "actual_delivery": delivery["actual_delivery"],

                        "batter_id": batter_id,
                        "bowler_id": bowler_id,
                        "non_striker_id": non_striker_id,

                        "batter_runs": batter_runs,
                        "extra_runs": extra_runs,
                        "extra_type": extra_type,
                        "total_runs": total_runs,

                        "is_wicket": is_wicket,
                        "wicket_kind": wicket_kind,
                        "player_out_id": player_out_id
                    })

    # print(f"Total Ball Records : {len(fact_ball_by_ball)}")
    # print(fact_ball_by_ball[:5])


    # DIM_MATCHES
    match_records = []

    for json_file in json_files:

        with open(json_file, "r", encoding="utf-8") as file:
            match_data = json.load(file)

        info = match_data["info"]
        match_id = json_file.stem

        season = str(info["season"])

        # Teams
        team1 = team_name_mapping.get(
            info["teams"][0],
            info["teams"][0]
        )

        team2 = team_name_mapping.get(
            info["teams"][1],
            info["teams"][1]
        )

        toss_winner = team_name_mapping.get(
            info["toss"]["winner"],
            info["toss"]["winner"]
        )

        winner = team_name_mapping.get(
            info["outcome"].get("winner"),
            info["outcome"].get("winner")
        )

        # Venue
        venue_name = venue_name_mapping.get(
            info["venue"],
            info["venue"]
        )

        # Event
        event = info.get("event", {})

        match_number = event.get("match_number")
        stage = event.get("stage")

        # Result
        win_by_runs = None
        win_by_wickets = None

        if "by" in info["outcome"]:
            win_by_runs = info["outcome"]["by"].get("runs")
            win_by_wickets = info["outcome"]["by"].get("wickets")

        match_records.append({

            "match_id": match_id,

            "match_date": info["dates"][0],

            "season": season,

            "match_number": match_number,

            "stage": stage,

            "overs": info["overs"],

            "balls_per_over": info["balls_per_over"],

            "venue_id": venue_lookup[venue_name],

            "team1_id": team_lookup[team1],

            "team2_id": team_lookup[team2],

            "toss_winner_team_id": team_lookup[toss_winner],

            "toss_decision": info["toss"]["decision"],

            "winner_team_id": (
                team_lookup[winner]
                if winner is not None
                else None
            ),

            "win_by_runs": win_by_runs,

            "win_by_wickets": win_by_wickets

        })

    # print(f"Total Matches : {len(match_records)}")
    # print(match_records[:5])

    return (
        team_records,
        venue_records,
        player_records,
        match_records,
        fact_ball_by_ball
    )