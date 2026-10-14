# STEP 5 - Build the team dashboard web page
# Problem: the team and managers don't read code - they need ONE link that shows
#          how fast requests get done, who sends the most, and what's still waiting.
# How: the page design lives in dashboard/template.html. It has a spot that says __DATA__.
#      This script works out the numbers, drops them into that spot, and saves docs/index.html.
#      GitHub Pages then shows docs/index.html as a website.

import os
import json
import pandas as pd
# NOTE: json = a way to write Python data (lists, dicts) as text a web page can read.

df = pd.read_csv("output/requests_clean.csv", parse_dates=["submitted_at"])
done = df[df["status"] == "Completed"]
still_open = df[df["status"] != "Completed"]
TARGETS = {"High": 1, "Medium": 3, "Low": 5}
# NOTE: Opened the clean data and split it into finished and still-open requests.
#       TARGETS = how many days each priority is supposed to take.

# ---------- the 4 headline numbers ----------
missed = 0
for priority, target in TARGETS.items():
    rows = done[done["priority"] == priority]
    missed = missed + (rows["turnaround_days"] > target).sum()
kpis = {
    "total": len(df),
    "duplicates": 5,
    "avg_days": round(done["turnaround_days"].mean(), 1),
    "median_days": round(done["turnaround_days"].median(), 1),
    "completed": len(done),
    "missed": int(missed),
    "missed_pct": round(100 * missed / len(done)),
    "open": len(still_open),
    "open_unassigned": int((still_open["assigned_to"] == "Unassigned").sum()),
    "never_started": int((still_open["status"] == "Open").sum()),
}
# NOTE: The loop counts late requests for each priority and adds them up.
#       never_started = requests with status "Open" - nobody has touched them yet.
#       duplicates = 5 is what Step 1 removed (the raw file had 305 rows, the clean one has 300).

# ---------- by priority ----------
by_priority = []
for priority, target in TARGETS.items():
    rows = done[done["priority"] == priority]
    by_priority.append({
        "priority": priority,
        "target": target,
        "avg_days": round(rows["turnaround_days"].mean(), 2),
        "completed": len(rows),
        "missed": int((rows["turnaround_days"] > target).sum()),
    })
# NOTE: For each priority: the average days, the target, how many finished, and how many were late.

# ---------- by team ----------
by_team = []
for team, count in df["team"].value_counts().items():
    open_count = (still_open["team"] == team).sum()
    by_team.append({"team": team, "requests": int(count), "open": int(open_count)})
# NOTE: value_counts() = requests per team, biggest first. Also counted each team's open ones.

# ---------- most common request type per team ----------
top_types = []
for team in df["team"].value_counts().index:
    types = df[df["team"] == team]["request_type"].value_counts()
    top = types[types == types.max()]
    top_types.append({"team": team, "type": " / ".join(top.index), "n": int(types.max())})
# NOTE: For each team, counted its request types and kept the top one (same answer as SQL Q6).
#       If 2 types tie, both are kept and joined with " / " - just like RANK does in SQL.

# ---------- on time by analyst and by team ----------
done = done.copy()
done["on_time"] = done["turnaround_days"] <= done["priority"].map(TARGETS)
on_time_analyst = []
for analyst, pct in (done.groupby("assigned_to")["on_time"].mean() * 100).sort_values().items():
    count = (done["assigned_to"] == analyst).sum()
    on_time_analyst.append({"name": analyst, "pct": round(pct, 1), "completed": int(count)})
on_time_team = []
for team, pct in (done.groupby("team")["on_time"].mean() * 100).sort_values().items():
    count = (done["team"] == team).sum()
    on_time_team.append({"name": team, "pct": round(pct, 1), "completed": int(count)})
# NOTE: True/False for "finished within its target", then the average per analyst and per team x100 = on-time %.
#       Sorted worst first, so whoever needs help is at the top.

# ---------- by month ----------
by_month = []
month_counts = df.groupby(df["submitted_at"].dt.strftime("%Y-%m")).size()
for month, count in month_counts.items():
    label = pd.to_datetime(month + "-01").strftime("%b %Y")
    by_month.append({"label": label, "requests": int(count)})
# NOTE: Counted requests per month. The label turns "2026-06" into "Jun 2026" so it reads nicely.

# ---------- open work ----------
as_of = pd.Timestamp("2026-09-29 08:00")
still_open = still_open.copy()
still_open["waiting"] = (as_of - still_open["submitted_at"]).dt.days
# NOTE: as_of = the day the export was pulled (same AS_OF date as Step 0). waiting = how many days each open request has been sitting there.

by_owner = []
for owner, count in still_open["assigned_to"].value_counts().items():
    oldest = still_open[still_open["assigned_to"] == owner]["waiting"].max()
    by_owner.append({"owner": owner, "open": int(count), "oldest": int(oldest)})
# NOTE: Open requests per analyst, plus how long their oldest one has been waiting.

open_list = []
for _, row in still_open.sort_values("waiting", ascending=False).iterrows():
    open_list.append({
        "id": row["request_id"],
        "team": row["team"],
        "type": row["request_type"],
        "priority": row["priority"],
        "owner": row["assigned_to"],
        "status": row["status"],
        "submitted": row["submitted_at"].strftime("%Y-%m-%d"),
        "waiting": int(row["waiting"]),
        "target": TARGETS[row["priority"]],
    })
# NOTE: Every open request with its details, longest waiting first - this becomes the searchable table.

# ---------- put it in the page ----------
data = {"kpis": kpis, "by_priority": by_priority, "by_team": by_team, "top_types": top_types,
        "on_time_analyst": on_time_analyst, "on_time_team": on_time_team,
        "by_month": by_month, "by_owner": by_owner, "open": open_list,
        "as_of": as_of.strftime("%b %d, %Y")}
template = open("dashboard/template.html").read()
page = template.replace("__DATA__", json.dumps(data))
os.makedirs("docs", exist_ok=True)
open("docs/index.html", "w").write(page)
open("docs/.nojekyll", "w").write("")
print("Saved docs/index.html -", len(open_list), "open requests in the list")
# NOTE: Packed everything into one dict, turned it into text with json.dumps,
#       and swapped it in where the template says __DATA__. Then saved the finished page.
#       .nojekyll is an empty file that tells GitHub Pages to show my page exactly as it is.
