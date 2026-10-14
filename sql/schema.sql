-- The table design: one row per data request.
-- DROP TABLE IF EXISTS = start fresh every run so rows don't get added twice.
DROP TABLE IF EXISTS requests;

CREATE TABLE requests (
    request_id        TEXT PRIMARY KEY,   -- REQ-1000 (PRIMARY KEY = can't repeat)
    submitted_at      TEXT,               -- when the request came in
    team              TEXT,               -- who asked (Operations, Finance, ...)
    request_type      TEXT,               -- ad hoc report, data pull, ...
    priority          TEXT,               -- High / Medium / Low
    assigned_to       TEXT,               -- the analyst working on it
    status            TEXT,               -- Completed / In Progress / Open
    completed_at      TEXT,               -- blank if not finished
    turnaround_hours  REAL                -- finish time minus start time
);
