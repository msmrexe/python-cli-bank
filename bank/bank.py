# bank.py

"""
Contains the main Bank controller class.

This class is responsible for:
- Managing all BankAccount objects.
- Loading accounts from and saving accounts to a CSV file.
- Handling actions *between* accounts, like transfers.
"""

import csv
import random
from .models import BankAccount

class Bank:
    """Manages all bank accounts and data persistence."""
    
    _CSV_HEADER = ['Customer', 'National ID', 'Acc Num', 'Credit']

    def __init__(self, db_path: str):
        self.db_path = db_path
        # Use a dictionary for fast lookups by account number
        self.accounts: dict[int, BankAccount] = {}

    def load_accounts(self):
        """
        Loads all accounts from the CSV database file.
        If the file doesn't exist, it will be created.
        """
        try:
            with open(self.db_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                try:
                    header = next(reader)
                    if header != self._CSV_HEADER:
                        print(f"Warning: CSV header mismatch. Expected {self._CSV_HEADER}")
                except StopIteration:
                    # File is empty, which is fine
                    return

                for row in reader:
                    if not row: continue # Skip empty lines
                    try:
                        name = row[0]
                        national_id = int(row[1])
                        acc_num = int(row[2])
                        balance = int(row[3])
                        
                        account = BankAccount(name, national_id, acc_num, balance)
                        self.accounts[acc_num] = account
                    except (ValueError, IndexError):
                        print(f"Warning: Skipping malformed row in CSV: {row}")

        except FileNotFoundError:
            print(f"Database file not found. A new one will be created at: {self.db_path}")
            # The file will be created on the first save

    def save_accounts(self):
        """Saves the current state of all accounts back to the CSV file."""
        try:
            with open(self.db_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self._CSV_HEADER)
                for acc in self.accounts.values():
                    writer.writerow([acc.name, acc.national_id, acc.acc_num, acc.balance])
        except IOError as e:
            print(f"Error: Could not save database to {self.db_path}. {e}")

    def _generate_unique_acc_num(self) -> int:
        """Generates a 9-digit account number that is not already in use."""
        while True:
            acc_num = random.randint(100000000, 999999999)
            if acc_num not in self.accounts:
                return acc_num

    def find_account_by_id(self, national_id: int) -> BankAccount | None:
        """Finds an account by the customer's national ID."""
        for acc in self.accounts.values():
            if acc.national_id == national_id:
                return acc
        return None

    def find_account(self, acc_num: int) -> BankAccount | None:
        """Finds an account by the account number."""
        return self.accounts.get(acc_num)

    def create_account(self, name: str, national_id: int, initial_deposit: int) -> BankAccount:
        """
        Creates a new bank account, saves it, and returns the object.

        Raises:
            ValueError: If an account with that ID already exists or
                        if the initial deposit is not positive.
        """
        if initial_deposit <= 0:
            raise ValueError("Initial deposit must be positive.")
        if self.find_account_by_id(national_id):
            raise ValueError("An account with this National ID already exists.")
        
        acc_num = self._generate_unique_acc_num()
        account = BankAccount(name, national_id, acc_num, initial_deposit)
        self.accounts[acc_num] = account
        self.save_accounts()  # Persist immediately
        return account

    def transfer(self, from_acc_num: int, to_acc_num: int, amount: int):
        """
        Transfers money from one account to another.

        This is an "atomic" operation: it either fully succeeds
        or fails completely, leaving balances unchanged.

        Args:
            from_acc_num (int): The sender's account number.
            to_acc_num (int): The receiver's account number.
            amount (int): The amount to transfer.

        Raises:
            ValueError: If accounts are not found, are the same,
                        or if the withdrawal fails.
        """
        if from_acc_num == to_acc_num:
            raise ValueError("Cannot transfer to the same account.")
            
        from_acc = self.find_account(from_acc_num)
        if not from_acc:
            raise ValueError(f"Sender account {from_acc_num} not found.")
            
        to_acc = self.find_account(to_acc_num)
        if not to_acc:
            raise ValueError(f"Receiver account {to_acc_num} not found.")

        # This is the core logic. We try to withdraw.
        # If it fails, it raises an exception and the deposit
        # never happens.
        try:
            from_acc.withdraw(amount)
            to_acc.deposit(amount)
            self.save_accounts()  # Save only if both actions succeed
        except ValueError as e:
            # Re-raise the error with more context
            raise ValueError(f"Transfer failed: {e}")
