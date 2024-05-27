import os
import random
import string

ACCOUNTS_FILE = "accounts.txt"

# Account class
class Account:
    def __init__(self, account_number, password, account_type, balance=0):
        self.account_number = account_number #account number 
        self.password = password
        self.account_type = account_type   #type of account Personal or Business
        self.balance = balance # Account balance

    def deposit(self, amount):  # method to deposit money into the account
        self.balance += amount

    def withdraw(self, amount): # method to withdraw money
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(self, target_account, amount):  # method to transfer money
        if amount > self.balance:
            return False
        self.withdraw(amount)
        target_account.deposit(amount)
        return True

class PersonalAccount(Account):   #PersonalAccount class inheriting from Account
    pass

class BusinessAccount(Account):   #BusinessAccount class inheriting from Account
    pass

class Bank:                  # Bank class to manage all accounts
    def __init__(self):
        self.accounts = self.load_accounts()

    def load_accounts(self):      # Method to load accounts from the file
        accounts = {}
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, 'r') as f:
                for line in f:
                    account_number, password, account_type, balance = line.strip().split(',')
                    balance = float(balance)
                    if account_type == 'Personal':
                        accounts[account_number] = PersonalAccount(account_number, password, account_type, balance)
                    elif account_type == 'Business':
                        accounts[account_number] = BusinessAccount(account_number, password, account_type, balance)
        return accounts

    def save_accounts(self):      # Method to save accounts to the file
        with open(ACCOUNTS_FILE, 'w') as f:
            for account in self.accounts.values():
                f.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")

    def create_account(self, account_type):  # Method to create a new account
        account_number = ''.join(random.choices(string.digits, k=10))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if account_type == 'Personal':
            account = PersonalAccount(account_number, password, account_type)
        elif account_type == 'Business':
            account = BusinessAccount(account_number, password, account_type)
        self.accounts[account_number] = account
        self.save_accounts()
        return account_number, password

    def login(self, account_number, password):       # Method to login to an account
        account = self.accounts.get(account_number)
        if account and account.password == password:
            return account
        return None

    def delete_account(self, account_number):     # method to delete a account
        if account_number in self.accounts:
            del self.accounts[account_number]
            self.save_accounts()
            return True
        return False

def main():              # Main function to run the banking application
    bank = Bank()
    while True:
        print("\nBanking System")
        print("1. Open Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':                        # Option to open a new account
            account_type = input("Enter account type (Personal/Business): ")
            account_number, password = bank.create_account(account_type)
            print(f"Account created. Account Number: {account_number}, Password: {password}")
        elif choice == '2':          # Option to login to an existing account
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            account = bank.login(account_number, password)
            if account:
                print("Login successful!")
                while True:
                    print("\n1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Transfer Money")
                    print("5. Delete Account")
                    print("6. Logout")
                    user_choice = input("Enter your choice: ")
                    if user_choice == '1':
                        print(f"Balance: {account.balance}")
                    elif user_choice == '2':          # Option to deposit money
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                        bank.save_accounts()
                        print(f"Deposited {amount}. New balance: {account.balance}")
                    elif user_choice == '3':         # Option to withdraw money
                        amount = float(input("Enter amount to withdraw: "))
                        if account.withdraw(amount):
                            bank.save_accounts()
                            print(f"Withdrew {amount}. New balance: {account.balance}")
                        else:
                            print("Insufficient funds.")
                    elif user_choice == '4':        # Option to transfer money to another account
                        target_account_number = input("Enter target account number: ")
                        amount = float(input("Enter amount to transfer: "))
                        target_account = bank.accounts.get(target_account_number)
                        if target_account:
                            if account.transfer(target_account, amount):
                                bank.save_accounts()
                                print(f"Transferred {amount} to {target_account_number}. New balance: {account.balance}")
                            else:
                                print("Insufficient funds.")
                        else:
                            print("Target account does not exist.")
                    elif user_choice == '5':           # Option to delete the account
                        confirm = input("Are you sure you want to delete your account? (yes/no): ")
                        if confirm.lower() == 'yes':
                            bank.delete_account(account_number)
                            print("Account deleted.")
                            break
                    elif user_choice == '6':      # Option to logout
                        break
                    else:
                        print("Invalid choice.")
            else:
                print("Invalid account number or password.")
        elif choice == '3':        # Option to exit the application
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()