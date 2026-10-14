# STEP 4 - Save the charts as pictures for the README
# Problem: GitHub can't show an Excel file, so anyone looking at my repo sees text but no chart.
#          Saving the charts as PNG images lets the README show them at the top.

import os
import pandas as pd
import matplotlib.pyplot as plt
# NOTE: matplotlib = the Python tool for drawing charts. pyplot (plt) is the part that draws them.

os.makedirs("images", exist_ok=True)
df = pd.read_csv("output/requests_clean.csv")
done = df[df["status"] == "Completed"]
# NOTE: Made an images folder, opened the clean data, and kept only finished requests
#       (open ones don't have a turnaround time yet).

BLUE = "#2a78d6"
DARK = "#0b0b0b"
GRAY = "#52514e"
# NOTE: The 3 colors I use - one blue for the bars, dark for titles, gray for labels.

# ---------- Chart 1: average turnaround vs. the target ----------
priorities = ["High", "Medium", "Low"]
targets = [1, 3, 5]
averages = []
missed = []
for p, t in zip(priorities, targets):
    rows = done[done["priority"] == p]
    averages.append(rows["turnaround_days"].mean())
    missed.append((rows["turnaround_days"] > t).mean() * 100)
# NOTE: For each priority I got 2 numbers: the average days, and the % of requests that went over the target.
#       Targets: High = 1 day, Medium = 3 days, Low = 5 days.
#       zip() walks through both lists together (High with 1, Medium with 3, Low with 5).
#       (rows > t).mean() = the share that's late, because True counts as 1 and False as 0.

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(priorities, averages, color=BLUE, width=0.5, label="Average days")
ax.scatter(priorities, targets, color=DARK, marker="_", s=1800, linewidths=2, label="Target")
for i in range(3):
    ax.text(i, averages[i] / 2, f"{averages[i]:.1f} days\n{missed[i]:.0f}% late",
            ha="center", va="center", fontsize=9, color="white")
# NOTE: Blue bar = average days. The black line on each bar = the target.
#       Inside each bar I wrote the average and the % that missed the target.

ax.set_title("Average days vs. target - High priority is fastest, but misses its target most often",
             loc="left", fontsize=11, color=DARK)
ax.set_ylabel("Days", color=GRAY)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(colors=GRAY)
ax.legend(frameon=False, loc="upper center", ncol=2, markerscale=0.4)
ax.set_ylim(0, 6.5)
plt.tight_layout()
plt.savefig("images/turnaround_vs_target.png", dpi=150)
plt.close()
# NOTE: Title, label, legend, removed the extra borders, and saved it as a picture.

# ---------- Chart 2: requests by team ----------
by_team = df["team"].value_counts().sort_values()
# NOTE: value_counts() counts how many requests each team sent. Sorted so the biggest is on top.

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.barh(by_team.index, by_team.values, color=BLUE, height=0.6)
for i, value in enumerate(by_team.values):
    ax.text(value + 1, i, str(value), va="center", fontsize=9, color=GRAY)
ax.set_title("Requests by team - Operations and Finance send over half",
             loc="left", fontsize=11, color=DARK)
ax.set_xlabel("Requests", color=GRAY)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(colors=GRAY)
ax.set_xlim(0, by_team.max() * 1.12)
plt.tight_layout()
plt.savefig("images/requests_by_team.png", dpi=150)
plt.close()
# NOTE: Sideways bars, one per team, with the count written at the end of each bar.

# ---------- Chart 3: on-time % by analyst ----------
TARGETS = {"High": 1, "Medium": 3, "Low": 5}
done = done.copy()
done["on_time"] = done["turnaround_days"] <= done["priority"].map(TARGETS)
on_time = (done.groupby("assigned_to")["on_time"].mean() * 100).sort_values(ascending=False)
# NOTE: Gave each finished request True/False for "finished within its target", then took the average per analyst.
#       The average of True/False = the share that's True, so x100 = on-time %. Sorted best first (best ends up at the bottom).

fig, ax = plt.subplots(figsize=(8, 2.8))
ax.barh(on_time.index, on_time.values, color=BLUE, height=0.55)
for i, value in enumerate(on_time.values):
    ax.text(value + 1, i, f"{value:.0f}%", va="center", fontsize=9, color=GRAY)
ax.set_title("On time by analyst - one analyst hits target less than half the time",
             loc="left", fontsize=11, color=DARK)
ax.set_xlabel("Finished within target (%)", color=GRAY)
ax.set_xlim(0, 100)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(colors=GRAY)
plt.tight_layout()
plt.savefig("images/on_time_by_analyst.png", dpi=150)
plt.close()
# NOTE: Sideways bars from 0 to 100%, with the % written at the end of each bar.

print("Saved 3 charts in the images folder")
