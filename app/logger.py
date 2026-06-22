import csv
import os
from datetime import datetime
from app.config import LOG_FOLDER

LOG_FILE = os.path.join(LOG_FOLDER, "rename_log.csv")


def write_log(old_name, new_name, status):
    """Write log entry to CSV file"""
    # Create log folder if not exists
    os.makedirs(LOG_FOLDER, exist_ok=True)

    # Check if file exists for headers
    file_exists = os.path.exists(LOG_FILE)

    try:
        with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write headers if new file
            if not file_exists:
                writer.writerow([
                    "datetime",
                    "old_name",
                    "new_name",
                    "status"
                ])

            # Write log entry
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                old_name,
                new_name,
                status
            ])
    except Exception as e:
        print(f"⚠️  Error writing log: {e}")