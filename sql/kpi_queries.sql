-- KPI QUERIES - the 8 questions people ask about the request log.
-- Pattern for almost all of them: filter (WHERE) -> group (GROUP BY) -> count or average -> sort (ORDER BY)


-- Q1 - Which team sends us the most work?
-- GROUP BY team = one row per team. COUNT(*) = how many rows (requests) each has.
SELECT team, COUNT(*) AS requests
FROM requests
GROUP BY team
ORDER BY requests DESC;


-- Q2 - Do High priority requests actually get done faster?
-- WHERE keeps only finished requests. AVG = average hours, divided by 24 to get days.
SELECT priority,
       COUNT(*) AS completed,
       ROUND(AVG(turnaround_hours) / 24, 1) AS avg_days
FROM requests
WHERE status = 'Completed'
GROUP BY priority
ORDER BY avg_days;


-- Q3 - How many requests missed their target?
-- Targets: High = 1 day (24 hours), Medium = 3 days (72), Low = 5 days (120).
-- CASE WHEN = an IF statement. It gives 1 if the request was late and 0 if not, then SUM adds up the 1s.
SELECT priority,
       SUM(CASE
             WHEN priority = 'High'   AND turnaround_hours > 24  THEN 1
             WHEN priority = 'Medium' AND turnaround_hours > 72  THEN 1
             WHEN priority = 'Low'    AND turnaround_hours > 120 THEN 1
             ELSE 0
           END) AS missed_target,
       COUNT(*) AS completed
FROM requests
WHERE status = 'Completed'
GROUP BY priority;


-- Q4 - Who has the most unfinished work right now?
-- <> means "not equal". So this keeps everything that isn't Completed, then counts per analyst.
SELECT assigned_to, COUNT(*) AS open_requests
FROM requests
WHERE status <> 'Completed'
GROUP BY assigned_to
ORDER BY open_requests DESC;


-- Q5 - How does volume change month to month?
-- strftime('%Y-%m', date) pulls out just the year and month (2026-06).
-- In SQL Server it would be FORMAT(submitted_at, 'yyyy-MM') instead.
SELECT strftime('%Y-%m', submitted_at) AS month,
       COUNT(*) AS requests
FROM requests
GROUP BY month
ORDER BY month;


-- Q6 - What does each team ask for the most?
-- This is the one harder query. 2 parts:
-- Part 1 (WITH counts AS ...) = count requests per team AND type. WITH just gives that result a name.
-- Part 2 = RANK() numbers each team's types from most to least (1 = most).
--   PARTITION BY team = restart the numbering for every team.
-- Then WHERE rnk = 1 keeps only the top type for each team.
-- If 2 types tie for the top spot, RANK gives them both a 1 - so both show up (that's why a team can appear twice).
WITH counts AS (
    SELECT team, request_type, COUNT(*) AS n
    FROM requests
    GROUP BY team, request_type
),
ranked AS (
    SELECT team, request_type, n,
           RANK() OVER (PARTITION BY team ORDER BY n DESC) AS rnk
    FROM counts
)
SELECT team, request_type, n
FROM ranked
WHERE rnk = 1
ORDER BY n DESC;


-- Q7 - Which analyst is on time most often? (and who might be overloaded)
-- WITH graded = first give every finished request a late flag (1 = late, 0 = on time), using the same targets as Q3.
-- Then GROUP BY analyst: SUM(late) = how many were late, and on_time_pct = the share that weren't.
-- 100.0 (not 100) makes SQL do decimal math instead of whole numbers.
WITH graded AS (
    SELECT assigned_to,
           CASE
             WHEN priority = 'High'   AND turnaround_hours > 24  THEN 1
             WHEN priority = 'Medium' AND turnaround_hours > 72  THEN 1
             WHEN priority = 'Low'    AND turnaround_hours > 120 THEN 1
             ELSE 0
           END AS late
    FROM requests
    WHERE status = 'Completed'
)
SELECT assigned_to,
       COUNT(*) AS completed,
       SUM(late) AS missed_target,
       ROUND(100.0 * (COUNT(*) - SUM(late)) / COUNT(*), 1) AS on_time_pct
FROM graded
GROUP BY assigned_to
ORDER BY on_time_pct;


-- Q8 - Which team's requests are on time most often?
-- Same idea as Q7, grouped by team instead of analyst.
WITH graded AS (
    SELECT team,
           CASE
             WHEN priority = 'High'   AND turnaround_hours > 24  THEN 1
             WHEN priority = 'Medium' AND turnaround_hours > 72  THEN 1
             WHEN priority = 'Low'    AND turnaround_hours > 120 THEN 1
             ELSE 0
           END AS late
    FROM requests
    WHERE status = 'Completed'
)
SELECT team,
       COUNT(*) AS completed,
       SUM(late) AS missed_target,
       ROUND(100.0 * (COUNT(*) - SUM(late)) / COUNT(*), 1) AS on_time_pct
FROM graded
GROUP BY team
ORDER BY on_time_pct;
