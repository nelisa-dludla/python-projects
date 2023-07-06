import csv
import random

def main():
    # Welcome Page
    print("""===== Welcome to Maze Bank =====

(l) Log In
(s) Sign Up
""")

    while True:
        user_input = input("Input: ").strip().lower()
        user_options = ["l", "s"]
        if user_input in user_options:
            if user_input == "l":
                login()
                break
            else:
                signup()
                break
        else:
            print("Invalid Input. Enter (l) to Log In to existing account or (s) to Sign Up for a new account.\n")

# For when user selects log in option
def login():
    print("\n===== Maze Bank - Log In ====\n")

    while True:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        valid_account = find_client_logins("clients.csv", username, password)
        # print(f"Both username and password are valid: {valid_account}")
        if valid_account:
            value = get_value_from_csv("clients.csv", "username", username, "accountNumber")
            account_page(value)

# For when user selects sign in option
def signup():
    print("\n===== Maze Bank - Sign Up ====\n")

    while True:
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        phone_number = input("Phone Number: ")
        email = input("email address: ")
        account_type = input('Account Type:\n(s) for "Savings" or (c) for "Cheque" ')

        print(f"""Account Details:

First Name: {first_name}
Last Name: {last_name}
Phone Number: {phone_number}
email address: {email}
Account Type: {account_type}
""")



# To look for client log ins in clients.csv file
def find_client_logins(file_name, username, password):
    valid_username = False
    valid_password = False
    with open(file_name, "r") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if row["username"] == username:
                valid_username = True
            else:
                print("Incorrect Username or Username does not exist")

            if row["password"] == password:
                valid_password = True
            else:
                print("Incorrect Password")

        if valid_username and valid_password:
            return True
        else:
            return False

# Displays client account page
def account_page(value):
    while True:
        account_balance = None
        client_name = None
        with open("accounts.csv", "r") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                if row["accountNumber"] == value:
                    account_balance = row["accountBalance"]
                    client_name = row["firstName"]
                    account_number = row["accountNumber"]



        print(f"""\n===== Maze Bank - Account =====\n
Welcome back, {client_name}

Account Number: {account_number}
Current Balance: {account_balance}

(d) Deposit
(t) Transfer
(w) Withdraw
""")

        user_options = ["d", "t", "w"]
        user_input = input("Input: ").strip().lower()
        if user_input in user_options:
            if user_input == "d":
                deposit(client_name)
            elif user_input == "t":
                transfer()
            else:
                withdraw()

# Displays deposit page
def deposit(client_name):
    print("\n===== Maze Bank - Deposit =====\n")

    while True:
        try:
            amount = float(input("Amount to be deposited: "))
        except ValueError:
            print("Invalid input. Make sure you have entered a value in numbers.")
        else:
            formatted_amount = format(amount, ".2f")
            value = get_value_from_csv("accounts.csv", "firstName", client_name, "accountBalance")
            new_amount = float(value) + amount
            formatted_new_amount = format(new_amount, ".2f")
            change_value_in_csv("accounts.csv", "accountBalance", str(value), formatted_new_amount)
            print(f"{formatted_amount} has been deposited into your account.")
            break


def transfer():
    print("From inside transfer function")


def withdraw():
    print("From inside withdraw function")

def generate_account_number():
    account_number = random.randint(1000000000, 9999999999)
    return account_number

def change_value_in_csv(filename, column_name, target_value, new_value):
    rows = []

    with open(filename, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        rows.append(header)

        for row in csv_reader:
            rows.append(rows)

    column_index = header.index(column_name)

    for row in rows:
        if row[column_index] == target_value:
            row[column_index] = new_value

    with open(filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rows)

def get_value_from_csv(filename, condition_column, condition_value, target_column):
    with open(filename, "r") as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            if row[condition_column] == condition_value:
                return row[target_column]



if __name__ == "__main__":
    main()