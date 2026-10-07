-- 03_advanced
-- Top 5 players by runs in each season

-- 14. Top 5 players by runs in each season

WITH player_season_runs AS (
    SELECT
        m.season,
        p.player_name,
        SUM(f.batter_runs) AS runs
    FROM fact_ball_by_ball f
    JOIN dim_players p
        ON f.batter_id = p.player_id
    JOIN dim_matches m
        ON f.match_id = m.match_id
    GROUP BY
        m.season,
        p.player_id,
        p.player_name
),

ranked_players AS (
    SELECT
        season,
        player_name,
        runs,
        RANK() OVER (
            PARTITION BY season
            ORDER BY runs DESC
        ) AS player_rank
    FROM player_season_runs
)

SELECT
    season,
    player_name,
    runs,
    player_rank
FROM ranked_players
WHERE player_rank <= 5
ORDER BY
    season,
    player_rank;