-- 1. Basic SQL — foundation
-- About 5 queries:

-- Total matches
select count(*) from dim_matches;

-- Total runs
select sum(total_runs) from fact_ball_by_ball;

-- Total wickets
select sum(is_wicket) AS wickets from fact_ball_by_ball;

-- Matches by season
select season, count(*) from dim_matches group by season order by season;

-- Wins by team
SELECT
    t.team_name,
    COUNT(*) AS wins
FROM dim_matches m
JOIN dim_teams t
    ON m.winner_team_id = t.team_id
WHERE m.winner_team_id IS NOT NULL
GROUP BY t.team_id, t.team_name
ORDER BY wins DESC;
