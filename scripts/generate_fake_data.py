# scripts/generate_fake_data.py

"""
Data Generation Script for the Bank of Wonderland.

This script generates a CSV file with fake user data to
populate the bank's database for testing and demonstration.

It requires the 'faker' library:
pip install faker
"""

import csv
import random
from faker import Faker

# --- Configuration ---
OUTPUT_FILE = 'Bank.csv'  # Saves to the root directory
NUM_ACCOUNTS = 50
CSV_HEADER = ['Customer', 'National ID', 'Acc Num', 'Credit']
# ---------------------

def generate_fake_data():
    """Generates and saves the fake account data to a CSV file."""
    
    print(f"Generating {NUM_ACCOUNTS} fake accounts...")
    
    fake = Faker()
    accounts_data = []
    
    # Use sets for fast uniqueness checks
    used_national_ids = set()
    used_acc_nums = set()

    while len(accounts_data) < NUM_ACCOUNTS:
        name = fake.name()
        
        # Generate a unique 10-digit national ID
        national_id = fake.random_int(min=1000000000, max=9999999999)
        if national_id in used_national_ids:
            continue
            
        # Generate a unique 9-digit account number
        acc_num = random.randint(100000000, 999999999)
        if acc_num in used_acc_nums:
            continue

        # Generate a positive initial balance
        balance = random.randint(500, 100000)

        # Add to sets and data list
        used_national_ids.add(national_id)
        used_acc_nums.add(acc_num)
        accounts_data.append([name, national_id, acc_num, balance])

    # Write the data to the CSV file
    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)
            writer.writerows(accounts_data)
        
        print(f"Successfully generated '{OUTPUT_FILE}' with {len(accounts_data)} accounts.")

    except IOError as e:
        print(f"Error: Could not write to file {OUTPUT_FILE}. {e}")

if __name__ == "__main__":
    generate_fake_data()
