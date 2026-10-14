# RUN EVERYTHING - one command rebuilds the whole project from scratch:
#   python run_all.py
# It runs each step in order. If any step fails, it stops right there so I can see which one broke.

import subprocess
import sys
# NOTE: subprocess = runs another Python file, the same as typing "python python/00_generate_data.py" myself.
#       sys.executable = the exact Python I'm using right now, so every step uses the same one.

STEPS = [
    "python/00_generate_data.py",
    "python/01_clean_data.py",
    "python/02_load_to_sql.py",
    "python/03_summary_report.py",
    "python/04_make_charts.py",
    "python/05_build_dashboard.py",
]
# NOTE: The 6 steps in the order they have to run - each one uses what the step before it saved.

for step in STEPS:
    print("\n========== Running", step, "==========")
    subprocess.run([sys.executable, step], check=True)
# NOTE: Runs each step and prints a header first so the output is easy to follow.
#       check=True = if a step crashes, stop everything instead of running the rest on bad data.

print("\nAll 6 steps done. Open output/request_summary.xlsx or docs/index.html to see the results.")
