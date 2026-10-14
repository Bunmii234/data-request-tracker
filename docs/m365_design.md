# How requests would come in - Microsoft 365 design

The Python + SQL part of this project is the back end (the analysis). This is how the front end - where requests come in - would work using no-code Microsoft 365 tools. It's a design, not something I built here.

## The setup

1. **Microsoft Forms - the front door.** Anyone who needs data fills out one form: team, request type, priority, description, due date. One place for every request instead of scattered emails and Teams messages.
2. **Power Automate - the connector.** When someone submits the form, a flow adds a new row to a SharePoint list, sets the status to "Open," and emails the person a confirmation. A second flow sends the team a reminder for anything still "Open" after 2 days with no owner.
3. **SharePoint List - the log.** One row per request with the owner, status, and dates. Analysts update the status as they work. This list has the same columns as `data/requests_raw.csv`.
4. **Power BI - the dashboard.** Connects to the SharePoint list and shows volume, turnaround, on-time %, and open work - the same numbers as `sql/kpi_queries.sql`.

## Before and after - what I'd measure

The sample data shows the problems this setup is meant to fix. These are the numbers I'd track before and after switching:

| What to measure | Before (sample data) | Goal after |
|---|---|---|
| Duplicate requests in the log | 5 | 0 - one form, one row per request |
| Team names typed different ways | 5 teams showed up as 9 spellings | 0 - the form uses a dropdown |
| Open requests with no owner | 4 | 0 - the reminder flow catches them within 2 days |
| Requests nobody started | 16 (oldest waited 113 days) | 0 older than a week |
| Finished requests that missed target | 29% | Under 15% |
| Analyst on-time gap | 47% vs. about 80% | Under 10 points apart - workload is visible, so it can be balanced |

**Why it matters:** requests stop getting lost, everyone can see what's being worked on, and turnaround gets measured instead of guessed.
