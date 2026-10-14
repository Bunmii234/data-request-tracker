# STEP 0 - Make the fake request log
# Problem: I can't use real work data (privacy), but I need realistic data to practice on.
# What this makes: a log of data requests that teams send to a reporting team -
#                  who asked, what for, how urgent, who's working on it, and when it got done.

import random
from datetime import datetime, timedelta
import pandas as pd
# NOTE: Loaded random (random numbers), datetime + timedelta (dates and lengths of time),
#       and pandas to save the table at the end.

random.seed(42)
# NOTE: Locked the random numbers to start point 42, so every run makes the exact same data.

TEAMS = ["Operations", "Finance", "Sales", "Business Development", "Compliance"]
TYPES = ["Ad hoc report", "Dashboard change", "Data pull", "Data correction", "Recurring report"]
ANALYSTS = ["Analyst A", "Analyst B", "Analyst C"]
START = datetime(2026, 6, 1, 8, 0)
AS_OF = START + timedelta(days=120)
# NOTE: The lists to pick from - 5 teams that send requests, 5 types of requests, 3 analysts.
#       START = June 1, 2026 at 8:00 AM, the first day of the log.
#       AS_OF = 120 days later (Sep 29) - the day I "pulled" this export. Anything not done by then is still open.

rows = []
for i in range(300):
    # NOTE: Loop 300 times - one time per request. Everything indented happens every time.

    submitted = START + timedelta(hours=random.randint(0, 120 * 24))
    team = random.choices(TEAMS, weights=[30, 25, 25, 10, 10])[0]
    request_type = random.choice(TYPES)
    priority = random.choices(["High", "Medium", "Low"], weights=[20, 50, 30])[0]
    analyst = random.choice(ANALYSTS)
    # NOTE: Picked the details for this request:
    #       submitted = a random hour in the 120 days after June 1.
    #       team = Operations sends the most (30%), Compliance the least (10%).
    #       priority = 20% High, 50% Medium, 30% Low.

    if priority == "High":
        hours = random.uniform(2, 36)
    elif priority == "Medium":
        hours = random.uniform(8, 96)
    else:
        hours = random.uniform(12, 150)
    if analyst == "Analyst B":
        hours = hours * 1.4
    # NOTE: How long it takes (in hours) depends on priority - High gets done fastest, Low slowest.
    #       Analyst B takes 40% longer - so the "on-time by analyst" check has something real to find
    #       (like someone who is overloaded).

    finished = submitted + timedelta(hours=hours)
    if finished > AS_OF:
        status = "In Progress"
        completed = ""
    elif random.random() < 0.05:
        status = "Open"
        completed = ""
    else:
        status = "Completed"
        completed = finished.strftime("%Y-%m-%d %H:%M")
    # NOTE: The status now makes sense with the dates:
    #       - if it would finish AFTER the export date, it's still "In Progress" (it came in recently)
    #       - 5% get "Open" - forgotten requests nobody started (these are the old ones to chase)
    #       - everything else is "Completed" with its finish time

    rows.append({
        "request_id": "REQ-" + str(1000 + i),
        "submitted_at": submitted.strftime("%Y-%m-%d %H:%M"),
        "team": team,
        "request_type": request_type,
        "priority": priority,
        "assigned_to": analyst,
        "status": status,
        "completed_at": completed,
    })
    # NOTE: Saved the request as one row (a dict with column names) in the rows list.
    #       IDs go REQ-1000, REQ-1001, ...

df = pd.DataFrame(rows)
# NOTE: Turned the list of 300 rows into a table (DataFrame).

for row in random.sample(range(300), 3):
    df.loc[row, "team"] = df.loc[row, "team"].upper()
for row in random.sample(range(300), 3):
    df.loc[row, "team"] = " " + df.loc[row, "team"].lower() + " "
not_done = list(df[df["status"] != "Completed"].index)
for row in random.sample(not_done, 4):
    df.loc[row, "assigned_to"] = ""
df = pd.concat([df, df.sample(5, random_state=1)], ignore_index=True)
# NOTE: Made it messy on purpose, like a real export:
#       3 team names in ALL CAPS, 3 in lowercase with extra spaces ("finance " instead of "Finance"),
#       4 unfinished requests with no analyst assigned (a finished one would always have someone),
#       and 5 rows copied again at the bottom (duplicates).

df.to_csv("data/requests_raw.csv", index=False)
print("wrote data/requests_raw.csv with", len(df), "rows")
# NOTE: Saved it - 305 rows (300 real + 5 duplicates).
