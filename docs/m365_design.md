# How requests would come in - Microsoft 365 design

The Python + SQL part of this project is the back end (the analysis). This is how the front end - where requests come in - would work using no-code Microsoft 365 tools.

1. **Microsoft Forms - the front door.** Anyone who needs data fills out one form: team, request type, priority, description, due date. One place for every request instead of scattered emails and Teams messages.
2. **Power Automate - the connector.** When someone submits the form, a flow adds a new row to a SharePoint list, sets the status to "Open," and emails the person a confirmation.
3. **SharePoint List - the log.** One row per request with the owner, status, and dates. Analysts update the status as they work. This list has the same columns as `data/requests_raw.csv`.
4. **Power BI - the dashboard.** Connects to the SharePoint list and shows volume, turnaround, and open work - the same numbers as `sql/kpi_queries.sql`.

**Why it matters:** requests stop getting lost, everyone can see what's being worked on, and turnaround gets measured instead of guessed.
