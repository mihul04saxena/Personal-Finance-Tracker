import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
from matplotlib import pyplot as plt


class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['Date', 'Amount', 'Category', 'Description']
    FORMAT = date_format = '%d-%m-%Y'

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            'Date': date,
            'Amount': amount,
            'Category': category,
            'Description': description
        }
        with open(cls.CSV_FILE, mode='a', newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print('Entry added successfully!')
    
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['Date'] = pd.to_datetime(df['Date'], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        filtered_df = df.loc[mask]
        if filtered_df.empty:
            print('No transactions found for the specified date range')
        else:
            print(f"Transactions between {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
            total_income = filtered_df[filtered_df['Category'] == 'Income']['Amount'].sum()
            total_expense = filtered_df[filtered_df['Category'] == 'Expense']['Amount'].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
        return filtered_df

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date (dd-mm-yyyy): or enter for today's date: ", allow_default=True)
    amount = get_amount("Enter the amount: ")
    category = get_category("Enter the category: ('I' for Income, 'E' for Expense) ")
    description = get_description("Enter the description: ")
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index('Date', inplace=True)

    income_df = (
        df[df['Category'] == 'Income']
        .resample('D')
        .sum()
        .reindex(df.index, fill_value=0)
    )

    expense_df = (
        df[df['Category'] == 'Expense']
        .resample('D')
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 6))
    plt.plot(income_df.index, income_df['Amount'], label='Income', color='green')
    plt.plot(expense_df.index, expense_df['Amount'], label='Expense', color='red')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Income and Expense Summary')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add a new Transaction")
        print("2. View Transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice(1-3): ")

        if choice == '1':
            add()
        elif choice == '2':
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if not df.empty and input("Do you want to plot the transactions? (y/n): ").lower() == 'y':
                plot_transactions(df)
        elif choice == '3':
            print('Exiting the program...')
            break
        else:
            print('Invalid choice. Please enter a number between 1 and 3')


if __name__ == '__main__':
    main()