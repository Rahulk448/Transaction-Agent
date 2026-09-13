from datetime import datetime
from transaction_agent import HistoricalTransaction
import csv
from transaction_agent import CustomerProfile
from profile import build_profile_summary


def parse_historical_transaction(row):
    return HistoricalTransaction(
        transaction_id=row["transaction_id"],
        customer_id=row["customer_id"],
        amount=int(row["amount"]) if row["amount"] else None,
        merchant=row["merchant"] if row["merchant"] else None,
        timestamp=datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M") if row["timestamp"] else None,
        location=row["location"] if row["location"] else None,
    )


def load_historical_transactions(filepath):
    transactions = []

    with open(filepath, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            transactions.append(parse_historical_transaction(row))

    return transactions

def group_by_customer(transactions):
    grouped = {}

    for transaction in transactions:
        customer_id = transaction.customer_id

        if customer_id not in grouped:
            grouped[customer_id] = []

        grouped[customer_id].append(transaction)

    return grouped


def build_customer_profiles(grouped_transactions):
    profiles = []

    for customer_id, transactions in grouped_transactions.items():
        profiles.append(
            CustomerProfile(
                customer_id=customer_id,
                historical_transactions=transactions,
            )
        )

    return profiles

def build_all_profile_summaries(profiles):
    summaries = []

    for profile in profiles:
        summaries.append(build_profile_summary(profile))

    return summaries