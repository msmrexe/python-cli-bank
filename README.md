# Simple CLI Bank Application

This project is a modular, CLI-based banking application written in Python. It was developed as a midterm project for an advanced Python programming course and has been structured with clarity, robustness, and extensibility in mind.

The application uses a simple CSV file as a database and follows a three-layer architecture (Model-View-Controller) to separate concerns.

## Features

* **Modular Design**: Code is split into `models.py` (data), `bank.py` (logic/controller), and `main.py` (UI/view).
* **Account Management**: Create new accounts with an initial deposit.
* **Account Access**: Log in to existing accounts using a unique account number.
* **Transactions**:
    * **Deposit**: Add funds to an account.
    * **Withdraw**: Remove funds, with checks for insufficient balance.
    * **Transfer**: A new feature to transfer funds between two accounts atomically.
* **Data Persistence**: All account data is loaded from and saved to a `.csv` file.
* **Robust Error Handling**: Uses exceptions (`try...except`) to handle invalid inputs (like non-numeric IDs) and failed business logic (like insufficient funds).
* **CLI Interface**: A clean, interactive command-line menu for all operations.

## Project Structure

```
simple-bank/
├── .gitignore         # Ignores data files and cache
├── LICENSE            # MIT license file
├── README.md          # This documentation
├── models.py          # Contains the BankAccount class (the "Model")
├── bank.py            # Contains the Bank class (the "Controller")
└── main.py            # The runnable script with all UI (the "View")
```

## Usage

You can run the application from your terminal.

### Standard Run

This will use the default `Bank.csv` file for storage.

```bash
python main.py
```

### Specifying a Database File

You can use the `--db` argument to specify a different file path for the account database.

```bash
python main.py --db production_bank.csv
```

---

## Author

Feel free to connect or reach out if you have any questions!

* **Maryam Rezaee**
* **GitHub:** [@msmrexe](https://github.com/msmrexe)
* **Email:** [ms.maryamrezaee@gmail.com](mailto:ms.maryamrezaee@gmail.com)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.
