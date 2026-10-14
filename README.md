# Data Request Tracker

**Python (pandas) · SQL · Excel** · fake data I generated - no real company data

**[Open the live dashboard](https://bunmii234.github.io/data-request-tracker/)**

## What it does

Takes a messy log of 305 data requests sent to a reporting team and answers what a manager asks: how fast do we finish, who's on time, and what's still waiting?

![On time by analyst](images/on_time_by_analyst.png)

## Results

- **2.4 days** average turnaround - but **29% missed their target**
- **High priority is fastest on average but misses its target most (36%)** - the average hides it
- **One analyst is on time 47%** vs. ~80% for the others - likely overloaded
- **16 requests never started** (oldest waited 113 days), 4 have no owner
- Operations and Finance send the most work

## How it works

1. **Generate** - 300 fake requests + duplicates, messy team names, blank owners
2. **Clean** (pandas) - remove duplicates, fix names, convert dates, flag missing owners
3. **Analyze** (SQL) - 8 KPI queries: volume, turnaround, missed targets, on-time % by analyst and team
4. **Report** - 5-sheet Excel file, 3 charts, and the live dashboard

## Problems I hit and how I fixed them

| Problem | Fix |
|---|---|
| 5 duplicate rows inflated every count | `drop_duplicates()` before anything else |
| 5 teams showed up as 9 spellings (`" finance "`, `"SALES"`) | `.str.strip().str.title()` |
| Blank owners | Labeled "Unassigned" instead of deleting - a manager needs to see them |
| First version had "open" requests waiting 100+ days for no reason | Status now follows the dates: recent = in progress, old = forgotten |
| Average turnaround looked fine and hid who was late | Added on-time % against a target, by analyst and by team |
| Two request types tied for a team's top spot | Used `RANK()`, which keeps ties instead of hiding one |
| GitHub can't show Excel, so nobody could see results | Added chart images and a live dashboard anyone can open |

## Limitations

Fake data - I made one analyst slower on purpose so the on-time check has something to find. Targets (1/3/5 days) are my choice, and turnaround counts calendar hours, not business hours.

## Run it

```
pip install -r requirements.txt
python run_all.py
```

SQL Server versions of the queries are in [`sql_server/`](sql_server/). The Microsoft 365 design for how requests would come in is in [`docs/m365_design.md`](docs/m365_design.md). Every code file has notes under each block explaining what it does.
