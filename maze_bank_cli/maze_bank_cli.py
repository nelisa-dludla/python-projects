import csv
import random
import sys
import re
import getpass

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
                login()
                break
        else:
            print("Invalid Input. Enter (l) to Log In to existing account or (s) to Sign Up for a new account.\n")

# For when user selects log in option
def login():
    print("\n===== Maze Bank - Log In =====\n")

    while True:
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()
        valid_account = find_client_logins("clients.csv", username, password)
        # print(f"Both username and password are valid: {valid_account}")
        if valid_account:
            account_number = get_value_from_csv("clients.csv", "username", username, "accountNumber")
            account_page(account_number)

# For when user selects sign in option
def signup():
    print("\n===== Maze Bank - Sign Up =====\n")

    while True:
        # First Name
        first_name = input("Enter your First Name: ").strip().title()
        while not is_valid_first_last(first_name):
            print("Invalid Input. First Name can only contain alphabets.")
            first_name = input("Enter your First Name: ").strip().title()
        # Last Name
        last_name = input("Enter your Last Name: ").strip().title()
        while not is_valid_first_last(last_name):
            print("Invalid Input. Last Name can only contain alphabets")
            last_name = input("Enter your Last Name: ").strip().title()
        # Phone Number
        phone_number = input("Enter your Phone Number: ").strip()
        while not is_valid_phone_number(phone_number):
            print("Invalid Input. Phone Number should be 10 digits long.")
            phone_number = input("Enter your Phone Number: ").strip()
        # Email
        email = input("Enter your email address: ").strip().lower()
        while not is_valid_email(email):
            print("Invalid input. Make sure you are using the valid email address format.")
            email = input("Enter your email address: ").strip().lower()
        # Account Type
        account_type = input('Choose an account Type:\n(s) for "Savings" or (c) for "Cheque"\nInput: ').strip().lower()
        while account_type not in ["s", "c"]:
            print("Invalid Input. Enter (s) to choose Savings or (c) to choose Cheque.")
            account_type = input('Choose an account Type:\n(s) for "Savings" or (c) for "Cheque" ').strip().lower()

        if account_type == "s":
            account_type = "Savings"
        else:
            account_type = "Cheque"
        # Username
        username = input("Enter a Username: ").strip()
        while not is_valid_username(username):
            print("Invalid Input. Username can only contain alphabets, numbers and/or an underscore.")
            username = input("Enter a Username: ")
        # Password
        password = input("Enter a Password: ").strip()
        while not is_valid_password(password):
            print("""Invalid Input.
Password must contain at least contain one alphabetical character (uppercase or lowercase)
Password must contain at least one digit
Password must be at least 8 characters long
""")
            password = input("Enter a Password: ").strip()
        # Generate account number for client
        account_number = generate_account_number()
        print(f"""\n===== Maze Bank - Account Details =====

Your account has been created.

Your Account Details are:

First Name: {first_name}
Last Name: {last_name}
Phone Number: {phone_number}
email address: {email}
Account Number: {account_number}
Account Type: {account_type}

You can now log in using:

username: {username}
password: {password}
""")
        # Write data into csv files
        store_data_in_csv(first_name, last_name, phone_number, email, account_type, account_number, username, password)
        # Exit sign in function
        break

# To look for client log ins in clients.csv file
def find_client_logins(file_name, username, password):
    valid_username = False
    valid_password = False
    with open(file_name, "r") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if row["username"] == username:
                valid_username = True

            if row["password"] == password:
                valid_password = True

    if valid_username and valid_password:
        return True
    elif not valid_username and valid_password:
            print("Incorrect Username or Username does not exist.")
            return False
    elif valid_username and not valid_password:
            print("Incorrect Password.")
            return False
    else:
        print("Incorrect Username or Username does not exist.")
        print("Incorrect Password")
        return False

# Displays client account page
def account_page(value):
    while True:
        account_balance = None
        client_name = None
        account_number = None
        # Retrieve client details
        with open("accounts.csv", "r") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                if row["accountNumber"] == value:
                    account_balance = row["accountBalance"]
                    client_name = row["firstName"]
                    account_type = row["accountType"]
                    account_number = row["accountNumber"]

        print(f"""\n===== Maze Bank - Account =====\n
Welcome back, {client_name}

Account Type: {account_type.title()}
Account Number: {account_number}
Current Balance: {account_balance}

(d) Deposit
(t) Transfer
(w) Withdraw

(q) Log Out and Exit
""")
        # Process User Input
        user_options = ["d", "t", "w", "q"]
        user_input = input("Input: ").strip().lower()
        if user_input in user_options:
            if user_input == "d":
                deposit(account_number)
            elif user_input == "t":
                transfer(account_number)
            elif user_input == "q":
                sys.exit("Logging Out...")
            else:
                withdraw(account_number)
        # User enters a character not in user_options
        else:
            print("Invalid Input.")

# Displays deposit page and processes the accountBalance change
def deposit(account_number):
    print("\n===== Maze Bank - Deposit =====\n")

    while True:
        try:
            amount = float(input("Amount to be deposited: "))
        except ValueError:
            print("Invalid input. Make sure you have entered a value in numbers.")
        else:
            formatted_amount = format(amount, ".2f")
            value = get_value_from_csv("accounts.csv", "accountNumber", account_number, "accountBalance")
            new_amount = float(value) + amount
            formatted_new_amount = format(new_amount, ".2f")
            change_value_in_csv("accounts.csv", "accountNumber", account_number, "accountBalance", formatted_new_amount)
            print(f"{formatted_amount} has been deposited into your account.")
            break

# Function displays transfer page and processes the accountBalance change
def transfer(account_number):
    print("\n===== Maze Bank - Transfer =====\n")

    while True:
        try:
            recipients_account = int(input("Account number of recipient: "))
            transfer_amount = float(input("Amount you want to transfer: "))
        except ValueError:
            print("Invalid input. Make sure you have entered a value in numbers.")
        else:
            formatted_transfer_amount = format(transfer_amount, ".2f")
            # Print verify tranaction page and get input from user
            print(f"\n===== Maze Bank - Verify Transaction =====\n\nTransfer {formatted_transfer_amount} to account number {recipients_account}? (y/n)")
            is_completed = False
            while not is_completed:
                user_input = input("Input: ").strip().lower()
                user_options = ["y", "n"]
                if user_input in user_options:
                    if user_input == "y" and is_valid_account(recipients_account):
                        # Find value of accountBalance for sender
                        sender_balance = get_value_from_csv("accounts.csv", "accountNumber", account_number, "accountBalance")
                        new_sender_balance = float(sender_balance) - float(formatted_transfer_amount)
                        new_sender_balance = format(new_sender_balance, ".2f")
                        # Check if sender has enough funds for transaction of requested amount
                        if float(new_sender_balance) < 0:
                            print("Insufficient funds. Transaction Cancelled.")
                            break
                        # Change value of accountBalance for sender
                        change_value_in_csv("accounts.csv", "accountNumber", account_number, "accountBalance", new_sender_balance)
                        # Find and change value of accountBalance for recipient
                        recipient_balance = get_value_from_csv("accounts.csv", "accountNumber", str(recipients_account), "accountBalance")
                        new_recipient_balance = float(recipient_balance) + float(formatted_transfer_amount)
                        new_recipient_balance = format(new_recipient_balance, ".2f")
                        change_value_in_csv("accounts.csv", "accountNumber", str(recipients_account), "accountBalance", new_recipient_balance)
                        is_completed = True
                        # Print success message
                        print("Transaction successful.")
                        break
                    # If the user confirms the transaction but the acconut doesn't exist
                    elif user_input == "y" and not is_valid_account(recipients_account):
                        print("Account number does not exist. Transaction cancelled.")
                        is_completed = True
                        break
                    # If the user selects (n)
                    else:
                        print("Transaction cancelled.")
                        is_completed = True
                        break
                else:
                    print("Invalid Input. Enter (y) for yes to confirm or (n) for no to cancel.\n")
            # Break out the main loop to take yo back to the account page
            break

# Function displays withdraw page and processes the accountBalance change
def withdraw(account_number):
    print("\n===== Maze Bank - Withdraw =====\n")

    while True:
        try:
            amount = float(input("Amount you want to withdraw: "))
        except ValueError:
            print("Invalid input. Make sure you have entered a value in numbers.")
        else:
            # Format withdrawal amount to 2 decimal places
            formatted_amount = format(amount, ".2f")
            # Retrieve accountBalance from csv and deduct amount from current accountBalance
            value = get_value_from_csv("accounts.csv", "accountNumber", account_number, "accountBalance")
            new_value = float(value) - amount
            # Check if account has enough funds for transaction of requested amount
            if new_value < 0:
                print("Insufficient funds.")
            else:
                # Format new amount to 2 decimal places
                formatted_new_amount = format(new_value, ".2f")
                # Change accountBalance to new amount
                change_value_in_csv("accounts.csv", "accountNumber", account_number, "accountBalance", formatted_new_amount)
                print(f"{formatted_amount} has been withdrawn from your account.")
            break

# Function generates an account number
def generate_account_number():
    account_number = random.randint(1000000000, 9999999999)
    return account_number

# Function changes the value inside a csv file
def change_value_in_csv(filename, condition_column, condition_value, target_column_name, new_value):
    rows = []
    # Open csv file and read its contents
    with open(filename, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        rows.append(header)
        # Copy contents inside csv to a list
        for row in csv_reader:
            rows.append(row)
    # Get index of relevant columns to find the value
    condition_column_index = header.index(condition_column)
    target_column_index = header.index(target_column_name)
    # Find value inside list and change it
    for row in rows:
        if row[condition_column_index] == condition_value:
            row[target_column_index] = new_value
    # Open csv file and write contents from list into the csv file
    with open(filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rows)

# Function retrieves a value from csv file
def get_value_from_csv(filename, condition_column, condition_value, target_column):
    # Open csv file and read its contents
    with open(filename, "r") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        # Find value and return it
        for row in csv_reader:
            if row[condition_column] == condition_value:
                return row[target_column]

# Function checks if account number exists
def is_valid_account(account_number):
    # Open csv file and read its contents
    with open("accounts.csv", "r") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        # Find value and return it
        for row in csv_reader:
            if row["accountNumber"] == str(account_number):
                return True
            elif row["accountNumber"] == None:
                return False

# Function checks if email is in the correct format
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Function checks if first/last name only contains alphabets
def is_valid_first_last(name):
    pattern = r"^[a-zA-Z].+$"
    return re.match(pattern, name) is not None

# Function checks if username contains valid characters
def is_valid_username(username):
    pattern = r"^[a-zA-Z0-9_]+$"
    return re.match(pattern, username) is not None

# Function checks if password meets requirements
def is_valid_password(password):
    pattern = r"^^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
    return re.match(pattern, password) is not None

# Function checks if the phone number only contains numbers and is 10 digits long
def is_valid_phone_number(phone_number):
    pattern = r"^[0-9]{,10}$"
    return re.match(pattern, phone_number) is not None

def store_data_in_csv(firstName, lastName, phoneNumber, email, accountType, accountNumber, username, password):
    # clients.csv
    with open("clients.csv", "r") as csvfile:
        # List to store contents from clients.csv
        rows = []
        # Open and read contents of clients.csv
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            rows.append(row)
        # New list to store data to be written into clients.csv
        clients_row = []
        clients_row.append(firstName)
        clients_row.append(lastName)
        clients_row.append(phoneNumber)
        clients_row.append(email)
        clients_row.append(accountType.lower())
        clients_row.append(accountNumber)
        clients_row.append(username)
        clients_row.append(password)
        rows.append(clients_row)
    # Write data into clients.csv
    with open("clients.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rows)

    # account.csv
    with open("accounts.csv", "r") as csvfile:
        # List to store contents of accounts.csv
        rows = []
        # Open and read contents of accounts.csv
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            rows.append(row)
        # New list to store data to be written into accounts.csv
        accounts_row = []
        accounts_row.append(firstName)
        accounts_row.append(lastName)
        accounts_row.append(accountType.lower())
        accounts_row.append(accountNumber)
        accounts_row.append(format(0.00, ".2f"))
        rows.append(accounts_row)
    # Write data into accounts.csv
    with open("accounts.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rows)


if __name__ == "__main__":
    main()