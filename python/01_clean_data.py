# STEP 1 - Clean the request log with pandas
# Problem: the raw export has duplicate rows, messy team names, blank owners, and dates stored as text.
#          If I report on it like this, every number after this is wrong.
# Same habit I use at work: check and clean the data before anything goes into a report.

import pandas as pd

df = pd.read_csv("data/requests_raw.csv")
print("Rows loaded:", len(df))
# NOTE: Opened the raw file as a table. 305 rows.

before = len(df)
df = df.drop_duplicates()
print("Duplicates removed:", before - len(df))
# NOTE: drop_duplicates() removed rows that are exact copies - same as Excel's Remove Duplicates button.
#       Counted rows before and after so I know how many came out (5).

df["team"] = df["team"].str.strip().str.title()
# NOTE: Fixed the team names: .str.strip() removes extra spaces (TRIM in Excel),
#       .str.title() makes it Capitalized Like This. So "finance " and "FINANCE" both become "Finance".
#       Without this, Finance shows up as 3 different teams in every count.

df["submitted_at"] = pd.to_datetime(df["submitted_at"])
df["completed_at"] = pd.to_datetime(df["completed_at"])
# NOTE: Turned the date text into real dates so I can subtract them. Blank finish times become NaT (empty date).

df["assigned_to"] = df["assigned_to"].fillna("Unassigned")
print("Unassigned requests:", (df["assigned_to"] == "Unassigned").sum())
# NOTE: Blank owners get the word "Unassigned" instead of being deleted -
#       a request with no owner is something a manager needs to SEE, not lose.

df["turnaround_hours"] = (df["completed_at"] - df["submitted_at"]).dt.total_seconds() / 3600
df["turnaround_days"] = (df["turnaround_hours"] / 24).round(2)
df["month"] = df["submitted_at"].dt.strftime("%Y-%m")
# NOTE: Added 3 new columns:
#       turnaround_hours = finish time - start time (seconds / 3600 = hours).
#       turnaround_days = the same in days. month = 2026-06, 2026-07... for monthly totals.

assert (df["turnaround_hours"].dropna() >= 0).all(), "Found a negative turnaround - check the dates"
print("Teams after cleaning:", sorted(df["team"].unique()))
# NOTE: Safety check - nothing can finish before it started. If it does, the script stops.
#       Then printed the team list to make sure there are exactly 5 now.

df.to_csv("output/requests_clean.csv", index=False)
print("Saved output/requests_clean.csv with", len(df), "rows")
# NOTE: Saved the clean version as a NEW file. The raw file never gets changed.
