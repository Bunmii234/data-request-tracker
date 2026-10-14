-- SQL SERVER (T-SQL) VERSION of sql/kpi_queries.sql
-- The project runs on SQLite. Most companies use SQL Server, so this file shows
-- the queries that need to be written differently there.
-- I haven't run this file on a real SQL Server - it's written for reference.
--
-- What's different from SQLite:
--   strftime('%Y-%m', date)   ->  FORMAT(date, 'yyyy-MM')
--   GROUP BY an alias         ->  SQL Server makes you repeat the full expression
--   ORDER BY inside a subquery isn't allowed without TOP
-- Q1, Q2, Q3, Q4, Q7 and Q8 work the same in both, so they aren't repeated here.


-- Q5 - Monthly volume
-- Different: FORMAT instead of strftime, and GROUP BY repeats the expression.
SELECT FORMAT(submitted_at, 'yyyy-MM') AS month,
       COUNT(*) AS requests
FROM requests
GROUP BY FORMAT(submitted_at, 'yyyy-MM')
ORDER BY month;


-- Q6 - Most common request type per team
-- Same idea (CTE + RANK). Written with 2 CTEs, which works the same in SQL Server.
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


-- Bonus - Top 5 slowest finished requests
-- Different: TOP 5 right after SELECT, instead of LIMIT 5 at the end.
SELECT TOP 5 request_id, team, priority, ROUND(turnaround_hours / 24, 1) AS days
FROM requests
WHERE status = 'Completed'
ORDER BY turnaround_hours DESC;
