import pandas as pd
import csv
import matplotlib.pyplot as plt
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


def plot_transactions(df):
    df.set_index("date", inplace=True)
    # Separate income and expenses into two DataFrames
    # This is done to plot them on the same graph
    # .resample("D") groups the data by day (fills in for missing days)
    # .sum() aggregate the rows that have the same date
    # .reindex() make sure that the new df conforms to the indexes of the original, filling blanks with 0 where needed
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


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
            if input("Do you want to see a plot? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
