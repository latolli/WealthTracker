import json
import os
from datetime import datetime

class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({"monthly_data": []}, file)

    def read_data(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def write_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def add_monthly_data(self, month_data):
        data = self.read_data()
        # Check if the month already exists
        for entry in data["monthly_data"]:
            if entry["month"] == month_data["month"]:
                # Update existing entry
                entry.update(month_data)
                break
        else:
            # If not found, append new data
            data["monthly_data"].append(month_data)

        # Sort the list based on the "month" field in ascending order (oldest to newest)
        data["monthly_data"].sort(key=lambda x: datetime.strptime(x["month"], "%Y-%m"))

        self.write_data(data)