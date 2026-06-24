-- ============================================================
-- World Cup Analytics Command Center
-- KPI Queries
-- ============================================================
--
-- This file contains analytical SQL queries designed to answer
-- business questions using the gold layer tables.
--
-- Main tables:
-- - fact_matches
-- - team_performance
-- - world_cup_summary_by_year
--
-- Note:
-- These queries are written in standard SQL style and may require
-- small syntax adjustments depending on the database engine used.
--
-- ============================================================


-- ============================================================
-- 1. World Cup summary by year
-- ============================================================
-- Business question:
-- How did the World Cup evolve over time in terms of matches,
-- goals and average goals per match?

SELECT
    year,
    matches,
    total_goals,
    ROUND(avg_goals_per_match, 2) AS avg_goals_per_match,
    host_countries,
    cities,
    teams
FROM world_cup_summary_by_year
ORDER BY year;


-- ============================================================
-- 2. Highest scoring World Cup editions
-- ============================================================
-- Business question:
-- Which World Cup editions had the highest number of goals?

SELECT
    year,
    total_goals,
    matches,
    ROUND(avg_goals_per_match, 2) AS avg_goals_per_match
FROM world_cup_summary_by_year
ORDER BY total_goals DESC;


-- ============================================================
-- 3. Average goals per match by decade
-- ============================================================
-- Business question:
-- How did scoring behavior change across decades?

SELECT
    decade,
    COUNT(*) AS matches,
    SUM(total_goals) AS total_goals,
    ROUND(AVG(total_goals), 2) AS avg_goals_per_match
FROM fact_matches
GROUP BY decade
ORDER BY decade;


-- ============================================================
-- 4. Teams with most World Cup matches
-- ============================================================
-- Business question:
-- Which teams have played the most World Cup matches historically?

SELECT
    team,
    SUM(matches_played) AS total_matches_played,
    SUM(wins) AS total_wins,
    SUM(draws) AS total_draws,
    SUM(losses) AS total_losses,
    SUM(goals_for) AS total_goals_for,
    SUM(goals_against) AS total_goals_against,
    SUM(goal_difference) AS total_goal_difference
FROM team_performance
GROUP BY team
ORDER BY total_matches_played DESC;


-- ============================================================
-- 5. Teams with most World Cup wins
-- ============================================================
-- Business question:
-- Which teams have won the most World Cup matches?

SELECT
    team,
    SUM(wins) AS total_wins,
    SUM(matches_played) AS total_matches_played,
    ROUND(SUM(wins) * 1.0 / SUM(matches_played), 3) AS historical_win_rate
FROM team_performance
GROUP BY team
HAVING SUM(matches_played) >= 10
ORDER BY total_wins DESC;


-- ============================================================
-- 6. Best historical win rate
-- ============================================================
-- Business question:
-- Which teams have the best win rate among teams with relevant
-- historical participation?

SELECT
    team,
    SUM(matches_played) AS total_matches_played,
    SUM(wins) AS total_wins,
    ROUND(SUM(wins) * 1.0 / SUM(matches_played), 3) AS historical_win_rate
FROM team_performance
GROUP BY team
HAVING SUM(matches_played) >= 10
ORDER BY historical_win_rate DESC;


-- ============================================================
-- 7. Best offensive teams
-- ============================================================
-- Business question:
-- Which teams scored the most goals historically in World Cups?

SELECT
    team,
    SUM(goals_for) AS total_goals_for,
    SUM(matches_played) AS total_matches_played,
    ROUND(SUM(goals_for) * 1.0 / SUM(matches_played), 2) AS goals_per_match
FROM team_performance
GROUP BY team
HAVING SUM(matches_played) >= 10
ORDER BY total_goals_for DESC;


-- ============================================================
-- 8. Best defensive teams
-- ============================================================
-- Business question:
-- Which teams conceded fewer goals per match?

SELECT
    team,
    SUM(goals_against) AS total_goals_against,
    SUM(matches_played) AS total_matches_played,
    ROUND(SUM(goals_against) * 1.0 / SUM(matches_played), 2) AS goals_against_per_match
FROM team_performance
GROUP BY team
HAVING SUM(matches_played) >= 10
ORDER BY goals_against_per_match ASC;


-- ============================================================
-- 9. Team performance by World Cup edition
-- ============================================================
-- Business question:
-- Which teams had the best performance in each World Cup edition?

SELECT
    year,
    team,
    matches_played,
    wins,
    draws,
    losses,
    goals_for,
    goals_against,
    goal_difference,
    points,
    ROUND(win_rate, 3) AS win_rate
FROM team_performance
ORDER BY
    year,
    points DESC,
    goal_difference DESC,
    goals_for DESC;


-- ============================================================
-- 10. Biggest wins by goal difference
-- ============================================================
-- Business question:
-- What were the biggest wins in World Cup history?

SELECT
    date,
    year,
    home_team,
    away_team,
    home_score,
    away_score,
    total_goals,
    ABS(goal_difference) AS absolute_goal_difference,
    city,
    country
FROM fact_matches
ORDER BY absolute_goal_difference DESC, total_goals DESC;


-- ============================================================
-- 11. Highest scoring matches
-- ============================================================
-- Business question:
-- Which matches had the highest total number of goals?

SELECT
    date,
    year,
    home_team,
    away_team,
    home_score,
    away_score,
    total_goals,
    city,
    country
FROM fact_matches
ORDER BY total_goals DESC;


-- ============================================================
-- 12. Result distribution
-- ============================================================
-- Business question:
-- What is the historical distribution of home wins, away wins
-- and draws in World Cup matches?

SELECT
    result,
    COUNT(*) AS matches,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM fact_matches
GROUP BY result
ORDER BY matches DESC;


-- ============================================================
-- 13. Neutral venue analysis
-- ============================================================
-- Business question:
-- Is there any difference in scoring behavior between neutral
-- and non-neutral venues?

SELECT
    neutral,
    COUNT(*) AS matches,
    SUM(total_goals) AS total_goals,
    ROUND(AVG(total_goals), 2) AS avg_goals_per_match
FROM fact_matches
GROUP BY neutral
ORDER BY neutral;


-- ============================================================
-- 14. Host country match volume
-- ============================================================
-- Business question:
-- Which countries hosted the most World Cup matches in the dataset?

SELECT
    country,
    COUNT(*) AS matches_hosted,
    COUNT(DISTINCT city) AS host_cities,
    COUNT(DISTINCT year) AS world_cup_editions
FROM fact_matches
GROUP BY country
ORDER BY matches_hosted DESC;


-- ============================================================
-- 15. City match volume
-- ============================================================
-- Business question:
-- Which cities hosted the most World Cup matches?

SELECT
    city,
    country,
    COUNT(*) AS matches_hosted,
    COUNT(DISTINCT year) AS world_cup_editions
FROM fact_matches
GROUP BY city, country
ORDER BY matches_hosted DESC;


-- ============================================================
-- 16. Team consistency across editions
-- ============================================================
-- Business question:
-- Which teams participated in the highest number of World Cup editions?

SELECT
    team,
    COUNT(DISTINCT year) AS world_cup_editions,
    SUM(matches_played) AS total_matches_played,
    SUM(points) AS total_points,
    SUM(wins) AS total_wins
FROM team_performance
GROUP BY team
ORDER BY world_cup_editions DESC, total_matches_played DESC;


-- ============================================================
-- 17. Historical points ranking
-- ============================================================
-- Business question:
-- Which teams have accumulated the most points historically?

SELECT
    team,
    SUM(points) AS total_points,
    SUM(matches_played) AS total_matches_played,
    SUM(wins) AS total_wins,
    SUM(draws) AS total_draws,
    SUM(losses) AS total_losses,
    SUM(goal_difference) AS total_goal_difference
FROM team_performance
GROUP BY team
ORDER BY total_points DESC;


-- ============================================================
-- 18. Most dominant team performances by edition
-- ============================================================
-- Business question:
-- Which team-year performances were the most dominant based on
-- points, goal difference and goals scored?

SELECT
    year,
    team,
    matches_played,
    points,
    wins,
    goals_for,
    goals_against,
    goal_difference,
    ROUND(win_rate, 3) AS win_rate
FROM team_performance
WHERE matches_played >= 3
ORDER BY
    points DESC,
    goal_difference DESC,
    goals_for DESC;


-- ============================================================
-- 19. Low scoring World Cup editions
-- ============================================================
-- Business question:
-- Which World Cup editions had the lowest average goals per match?

SELECT
    year,
    matches,
    total_goals,
    ROUND(avg_goals_per_match, 2) AS avg_goals_per_match
FROM world_cup_summary_by_year
ORDER BY avg_goals_per_match ASC;


-- ============================================================
-- 20. Potential data quality check: duplicated matches
-- ============================================================
-- Business question:
-- Are there duplicated match records based on date, home team
-- and away team?

SELECT
    date,
    home_team,
    away_team,
    COUNT(*) AS records
FROM fact_matches
GROUP BY
    date,
    home_team,
    away_team
HAVING COUNT(*) > 1
ORDER BY records DESC;