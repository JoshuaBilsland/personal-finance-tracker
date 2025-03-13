import pandas as pd
import csv
from datetime import datetime


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]

    @classmethod
    def initialise_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            # Make DataFrame with the four columns
            df = pd.DataFrame(columns=cls.COLUMNS)
            # Create CSV from the DataFrame
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, mode="a", newline="") as csvfile:
            # Create a CSV writer which lets you write dictionaries into the file
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully!")


CSV.initialise_csv()
CSV.add_entry("13/03/2025", 9.60, "Expense", "Food")
