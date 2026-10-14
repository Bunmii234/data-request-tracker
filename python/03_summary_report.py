# STEP 3 - Build the summary a manager would actually read
# Problem: managers don't open databases. They want one Excel file with the key numbers.

import pandas as pd

df = pd.read_csv("output/requests_clean.csv")
done = df[df["status"] == "Completed"]
# NOTE: Opened the clean data. done = only the finished requests (a filter),
#       because open requests don't have a turnaround time yet.

kpis = pd.DataFrame({
    "Metric": ["Total requests", "Completed", "Still open", "Avg turnaround (days)", "Median turnaround (days)"],
    "Value": [len(df), len(done), len(df) - len(done),
              round(done["turnaround_days"].mean(), 1), round(done["turnaround_days"].median(), 1)],
})
# NOTE: The 5 headline numbers. Mean = average. Median = the middle value -
#       it doesn't get pulled up by a few requests that took forever, so I show both.

by_team = done.groupby("team")["turnaround_days"].agg(["count", "mean"]).round(1)
by_team = by_team.sort_values("count", ascending=False)
# NOTE: groupby = a PivotTable. One row per team: how many requests they had finished and the average days.

monthly = df.pivot_table(index="month", columns="team", values="request_id", aggfunc="count", fill_value=0)
# NOTE: pivot_table = an actual PivotTable - months down the side, teams across the top, count of requests inside.

TARGETS = {"High": 1, "Medium": 3, "Low": 5}
done = done.copy()
done["target_days"] = done["priority"].map(TARGETS)
done["on_time"] = done["turnaround_days"] <= done["target_days"]
by_analyst = (done.groupby("assigned_to")["on_time"].agg(["count", "mean"])
              .rename(columns={"count": "completed", "mean": "on_time_pct"}))
by_analyst["on_time_pct"] = (by_analyst["on_time_pct"] * 100).round(1)
team_on_time = (done.groupby("team")["on_time"].agg(["count", "mean"])
                .rename(columns={"count": "completed", "mean": "on_time_pct"}))
team_on_time["on_time_pct"] = (team_on_time["on_time_pct"] * 100).round(1)
# NOTE: Same idea as SQL Q7 and Q8, but in pandas:
#       .map(TARGETS) looks up each request's target, on_time = True if it finished within it.
#       The mean of True/False = the share that's True (True counts as 1), so x100 = on-time %.

with pd.ExcelWriter("output/request_summary.xlsx") as xl:
    kpis.to_excel(xl, sheet_name="KPIs", index=False)
    by_team.to_excel(xl, sheet_name="By team")
    monthly.to_excel(xl, sheet_name="Monthly volume")
    by_analyst.sort_values("on_time_pct").to_excel(xl, sheet_name="On time by analyst")
    team_on_time.sort_values("on_time_pct").to_excel(xl, sheet_name="On time by team")
# NOTE: Wrote the 5 tables into one Excel file, one sheet each.

print(kpis.to_string(index=False))
print(); print(by_analyst)
print()
print(by_team)
print("\nSaved output/request_summary.xlsx")
# NOTE: Printed the results so I can check them without opening Excel.
