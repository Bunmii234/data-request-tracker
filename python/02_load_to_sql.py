# STEP 2 - Put the clean data in a SQL database and run the KPI queries
# Problem: people keep asking the same questions - how fast do we finish requests,
#          who's waiting the longest, which team sends the most work?
#          The answers live in sql/kpi_queries.sql. This script loads the data and runs them.

import sqlite3
import pandas as pd
# NOTE: sqlite3 = a small SQL database that lives in one file (built into Python).

df = pd.read_csv("output/requests_clean.csv")
con = sqlite3.connect("output/requests.db")
con.executescript(open("sql/schema.sql").read())
# NOTE: Opened the clean data, created/connected to the database file, and ran schema.sql to build the empty table.

columns = ["request_id", "submitted_at", "team", "request_type", "priority",
           "assigned_to", "status", "completed_at", "turnaround_hours"]
df[columns].to_sql("requests", con, if_exists="append", index=False)
print("Loaded", len(df), "rows into SQLite\n")
# NOTE: Picked the 9 columns the table has and loaded the rows into it.

queries = open("sql/kpi_queries.sql").read().split(";")
for query in queries:
    if query.strip() != "":
        print(pd.read_sql(query, con).to_string(index=False), "\n")
con.close()
# NOTE: Cut the .sql file into separate queries at every ";" and ran them one by one, printing each answer.
#       if query.strip() != "" skips the empty piece after the last ";". Then closed the database.
