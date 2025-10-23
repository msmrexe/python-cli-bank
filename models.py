# models.py

"""
Contains the data model for a single BankAccount.

This class is responsible for managing its own state and
enforcing its own business rules (e.g., preventing
overdrafts).
"""

class BankAccount:
    """Represents a single customer bank account."""

    def __init__(self, name: str, national_id: int, acc_num: int, balance: int):
        self._name = name
        self._national_id = national_id
        self._acc_num = acc_num
        self._balance = balance

    def __repr__(self) -> str:
        """Provides a clean string representation of the account."""
        return f"<BankAccount(Name='{self.name}', ID={self.id}, AccNum={self.acc_num}, Balance={self.balance})>"

    # --- Public Properties (Read-Only) ---

    @property
    def name(self) -> str:
        return self._name

    @property
    def national_id(self) -> int:
        return self._national_id

    @property
    def acc_num(self) -> int:
        return self._acc_num

    @property
    def balance(self) -> int:
        return self._balance

    # --- Public Methods ---

    def get_summary(self) -> str:
        """Returns a human-readable summary string."""
        return (
            f"Customer Name:   {self.name}\n"
            f"National ID:     {self.national_id}\n"
            f"Account Number:  {self.acc_num}\n"
            f"Balance:         {self.balance} Rial"
        )

    def deposit(self, amount: int):
        """
        Deposits a positive amount into the account.

        Args:
            amount (int): The amount to deposit.

        Raises:
            ValueError: If the amount is zero or negative.
        """
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        self._balance += amount

    def withdraw(self, amount: int):
        """
        Withdraws a positive amount from the account.

        Args:
            amount (int): The amount to withdraw.

        Raises:
            ValueError: If the amount is zero, negative,
                        or greater than the current balance.
        """
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if amount > self._balance:
            raise ValueError(f"Insufficient funds. Current balance is {self._balance}.")
        if amount == self._balance:
             raise ValueError("Withdrawal amount cannot be equal to the current balance. You cannot empty your account.")

        self._balance -= amount
