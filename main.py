import pandas as pd
import csv
from datetime import datetime
from data_entry import DATE_FORMAT, get_date, get_amount, get_category, get_description

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

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        # Convert the data to a datetime object
        df["date"] = pd.to_datetime(df["date"], format=DATE_FORMAT)
        start_date = datetime.strptime(start_date, DATE_FORMAT)
        end_date = datetime.strptime(end_date, DATE_FORMAT)

        # Create a mask to filter for transactions between the two dates
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found for the given date range.")
            return
        else:
            print(
                f"Transactions from {start_date.strftime(DATE_FORMAT)} to {end_date.strftime(DATE_FORMAT)}"
            )
            print(
                filtered_df.to_string(index=False, formatters={
                    "date": lambda x: x.strftime(DATE_FORMAT),
                    "amount": lambda x: f"{x:.2f}"
                })
            )

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("----------")
            print(f"Total Income: £{total_income:.2f}")
            print(f"Total Expense: £{total_expense:.2f}")
            print(f"Net Savings: £{(total_income - total_expense):.2f}")
            return filtered_df
            
            
def add():
    CSV.initialise_csv()
    date = get_date("Enter the date of transaction (dd/mm/yyyy) or enter for today's date: ",
                    allow_default=True
                    )
    amount = get_amount()
    category = get_category()
    desciption = get_description()
    CSV.add_entry(date, amount, category, desciption)


def main():
    while True:
        print("\n1. Add a transaction")
        print("2. View transactions withing a date range")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd/mm/yyyy): ")
            end_date = get_date("Enter the end date (dd/mm/yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
