-- Intermediate SQL — joins + cricket analysis

-- Team performance — matches, wins, losses, win %
SELECT
    t.team_name,
    COUNT(*) AS matches_played,
    SUM(CASE
        WHEN m.winner_team_id = t.team_id THEN 1
        ELSE 0
    END) AS wins,
    SUM(CASE
        WHEN m.winner_team_id != t.team_id THEN 1
        ELSE 0
    END) AS losses,
    ROUND(
        100.0 * SUM(CASE
            WHEN m.winner_team_id = t.team_id THEN 1
            ELSE 0
        END) / COUNT(*),
        2
    ) AS win_percentage
FROM dim_teams t
JOIN dim_matches m
    ON t.team_id = m.team1_id
    OR t.team_id = m.team2_id
GROUP BY t.team_id, t.team_name
ORDER BY win_percentage DESC;

-- Player runs
SELECT
    p.player_name,
    SUM(f.batter_runs) AS runs
FROM fact_ball_by_ball f
JOIN dim_players p
    ON f.batter_id = p.player_id
GROUP BY p.player_id, p.player_name
ORDER BY runs DESC;


-- Player wickets
SELECT
    p.player_name,
    COUNT(*) AS wickets
FROM fact_ball_by_ball f
JOIN dim_players p
    ON f.player_out_id = p.player_id
WHERE f.is_wicket = 1
GROUP BY p.player_id, p.player_name
ORDER BY wickets DESC;


-- Venue performance
SELECT
    v.venue_name,
    COUNT(DISTINCT m.match_id) AS matches,
    SUM(f.total_runs) AS total_runs
FROM dim_venues v
JOIN dim_matches m
    ON v.venue_id = m.venue_id
JOIN fact_ball_by_ball f
    ON m.match_id = f.match_id
GROUP BY v.venue_id, v.venue_name
ORDER BY total_runs DESC;

-- Toss vs match result
SELECT
    COUNT(*) AS total_matches,
    SUM(CASE
        WHEN toss_winner_team_id = winner_team_id THEN 1
        ELSE 0
    END) AS toss_winner_won,
    ROUND(
        100.0 * SUM(CASE
            WHEN toss_winner_team_id = winner_team_id THEN 1
            ELSE 0
        END) / COUNT(*),
        2
    ) AS toss_win_percentage
FROM dim_matches
WHERE winner_team_id IS NOT NULL;

-- Batting strike rate
SELECT
    p.player_name,
    SUM(f.batter_runs) AS runs,
    COUNT(*) AS balls,
    ROUND(
        100.0 * SUM(f.batter_runs) / COUNT(*),
        2
    ) AS strike_rate
FROM fact_ball_by_ball f
JOIN dim_players p
    ON f.batter_id = p.player_id
GROUP BY p.player_id, p.player_name
HAVING COUNT(*) >= 100
ORDER BY strike_rate DESC;

-- Bowling economy
SELECT
    p.player_name,
    SUM(f.total_runs) AS runs_conceded,
    COUNT(*) AS balls,
    ROUND(
        6.0 * SUM(f.total_runs) / COUNT(*),
        2
    ) AS economy
FROM fact_ball_by_ball f
JOIN dim_players p
    ON f.bowler_id = p.player_id
GROUP BY p.player_id, p.player_name
HAVING COUNT(*) >= 300
ORDER BY economy ASC;

-- Season-wise player performance
SELECT
    m.season,
    p.player_name,
    SUM(f.batter_runs) AS runs
FROM fact_ball_by_ball f
JOIN dim_players p
    ON f.batter_id = p.player_id
JOIN dim_matches m
    ON f.match_id = m.match_id
GROUP BY m.season, p.player_id, p.player_name
ORDER BY m.season, runs DESC;