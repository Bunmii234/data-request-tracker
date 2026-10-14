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

with pd.ExcelWriter("output/request_summary.xlsx") as xl:
    kpis.to_excel(xl, sheet_name="KPIs", index=False)
    by_team.to_excel(xl, sheet_name="By team")
    monthly.to_excel(xl, sheet_name="Monthly volume")
# NOTE: Wrote the 3 tables into one Excel file, one sheet each.

print(kpis.to_string(index=False))
print()
print(by_team)
print("\nSaved output/request_summary.xlsx")
# NOTE: Printed the results so I can check them without opening Excel.
