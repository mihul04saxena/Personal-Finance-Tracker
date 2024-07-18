from datetime import datetime

date_format = '%d-%m-%Y'
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and date_str == '':
        return datetime.now().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print('Invalid date format. Please enter a date in the format dd-mm-yyyy')
        return get_date(prompt, allow_default)

def get_amount(prompt):
    try:
        amount = float(input(prompt))
        if amount <= 0:
            raise ValueError('Amount must be greater than 0')
        return amount
    except ValueError as e:
        print(f'Invalid amount. {e}')
        return get_amount()

def get_category(prompt):
    category = input("Enter the category: ('I' for Income, 'E' for Expense) ").upper()
    if category not in CATEGORIES.keys():
        print('Invalid category. Please enter "I" for Income or "E" for Expense')
        return get_category(prompt)
    else:
        return CATEGORIES[category]

def get_description(prompt):
    return input(prompt)