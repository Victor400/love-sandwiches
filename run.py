import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

# ---- GOOGLE API SETUP ----
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# ---- OPTIONAL: View Existing Sales Data ----
sales = SHEET.worksheet('sales')
data = sales.get_all_values()
print("Current sales data:\n")
pprint(data)


# ---- FUNCTION DEFINITIONS ----

def get_sales_data():
    """
    Get sales figures input from the user.
    Loops until valid input is received.
    """
    while True:
        print("\nPlease enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Validates that exactly 6 integer values are provided.
    Returns True if valid, False otherwise.
    """
    try:
        if len(values) != 6:
            raise ValueError(f"Exactly 6 values required, you provided {len(values)}")

        [int(value) for value in values]  # Conversion test

    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Updates the given worksheet with the provided data row.
    """
    print(f"Updating '{worksheet}' worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"'{worksheet}' worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Calculate the surplus for each item type.
    Surplus = stock - sales
    Positive -> Waste, Negative -> Sold out (made extra)
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


# ---- MAIN FUNCTION ----

def main():
    """
    Runs all main program functions in order.
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")

    surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(surplus_data, "surplus")


# ---- RUN ----

print("Welcome to Love Sandwiches Data Automation")
main()
