from datetime import datetime

DATE_FORMAT = "%d/%m/%Y"
CATEGORIES = ["I": "Income", "E": "Expense"]

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(DATE_FORMAT)

    try:
        valid_date = datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        print("Invalid format! Enter date in dd/mm/yyyy format.")
        return get_date(prompt, allow_default)
    else:
        return valid_date.strftime(DATE_FORMAT)


def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category = input("Enter the category: ('I' for Income, 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("Invalid category! Choose from 'I' or 'E'.")
    return get_category()


def get_description():
    return input("Enter a description (optional): ")
