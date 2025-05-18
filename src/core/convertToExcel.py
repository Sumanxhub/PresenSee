import pandas as pd
import os
from datetime import datetime

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ATTENDANCE_DIR = os.path.join(BASE_DIR, "attendance")
DATABASE_DIR = os.path.join(BASE_DIR, "database")

# Get today's date file
today_str = datetime.now().strftime("%d-%B-%Y")
csv_file = os.path.join(ATTENDANCE_DIR, f"{today_str}.csv")
xlsx_file = os.path.join(DATABASE_DIR, f"{today_str}.xlsx")

# Convert to Excel
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    df.to_excel(xlsx_file, index=False)
    print(f"Converted '{csv_file}' to '{xlsx_file}'.")
else:
    print(f"No CSV file found for today: {csv_file}")
