# main.py

"""
Main entry point for the Bank of Merryland CLI.

This file handles all user interaction (menus, prompts)
and coordinates with the Bank controller to execute
user commands.
"""

import argparse
from bank import Bank
from models import BankAccount

def get_int_input(prompt: str) -> int:
    """Continuously prompts for an integer until one is given."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Oops! Input must be an integer. Please try again.")

def run_account_menu(account: BankAccount, bank: Bank):
    """
    Displays the menu for a logged-in user.
    
    Args:
        account: The BankAccount object for the logged-in user.
        bank: The main Bank controller object.
    """
    print(f"\nWelcome, {account.name}!")
    while True:
        print("""\n--- Account Menu ---
  1 ) Show info
  2 ) Deposit
  3 ) Withdraw
  4 ) Transfer
  5 ) Exit account""")
        choice = input("Enter number of option: ")

        if choice == '1':
            print("\n--- Account Details ---")
            print(account.get_summary())

        elif choice == '2':
            try:
                amount = get_int_input("Enter amount to deposit (in Rial): ")
                account.deposit(amount)
                bank.save_accounts()
                print(f"Deposit successful! New balance: {account.balance} Rial")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '3':
            try:
                amount = get_int_input("Enter amount to withdraw (in Rial): ")
                account.withdraw(amount)
                bank.save_accounts()
                print(f"Withdrawal successful! New balance: {account.balance} Rial")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '4':
            print("\n--- Transfer Funds ---")
            try:
                to_acc_num = get_int_input("Enter recipient's account number: ")
                amount = get_int_input("Enter amount to transfer (in Rial): ")
                bank.transfer(account.acc_num, to_acc_num, amount)
                print(f"Transfer successful! Your new balance: {account.balance} Rial")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '5':
            print("Have a nice day! Returning to main menu...\n")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


def main():
    """Runs the main application loop."""
    parser = argparse.ArgumentParser(description="Welcome to the Bank of Wonderland!")
    parser.add_argument(
        '--db',
        type=str,
        default='Bank.csv',
        help="Path to the bank's CSV database file (default: Bank.csv)"
    )
    args = parser.parse_args()

    print("Welcome to the Bank of Wonderland!")
    
    bank = Bank(db_path=args.db)
    try:
        bank.load_accounts()
        print(f"Loaded {len(bank.accounts)} accounts from {args.db}")
    except Exception as e:
        print(f"Fatal Error: Could not load database. {e}")
        return

    while True:
        print("""\n--- Main Menu ---
  1 ) Create an account
  2 ) Log in to existing account
  3 ) Exit program""")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\n--- Create New Account ---")
            try:
                name = input("Enter customer name: ")
                national_id = get_int_input("Enter national ID number: ")
                credit = get_int_input("Enter initial deposit amount (in Rial): ")
                
                account = bank.create_account(name, national_id, credit)
                print(f"Account was successfully created! *winky face*")
                print(f"Your new account number is: {account.acc_num}")
                print("Returning to main menu...")
            except ValueError as e:
                print(f"Error: {e}. Returning to main menu.\n")

        elif choice == '2':
            print("\n--- Account Login ---")
            acc_num = get_int_input("Enter account number: ")
            
            account = bank.find_account(acc_num)
            if account:
                run_account_menu(account, bank)
            else:
                print("No matching account. Check your info and try again.\n")

        elif choice == '3':
            print("\nThank you for banking with the Bank of Wonderland!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 3.")

if __name__ == '__main__':
    main()
