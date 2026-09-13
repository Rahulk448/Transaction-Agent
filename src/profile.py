"""Customer profile summary logic."""

from statistics import median

from transaction_agent import CustomerProfile, ProfileSummary


def calculate_typical_amount(profile: CustomerProfile) -> float | None:
    """Calculate the median amount from usable historical transactions."""
    amounts = [
        transaction.amount
        for transaction in profile.historical_transactions
        if transaction.amount is not None
    ]

    if not amounts:
        return None

    return median(amounts)


def calculate_common_merchants(profile: CustomerProfile) -> list[str]:
    """Return unique merchants in the order they first appeared."""
    merchants = []

    for transaction in profile.historical_transactions:
        if transaction.merchant is not None and transaction.merchant not in merchants:
            merchants.append(transaction.merchant)

    return merchants

def calculate_typical_locations(profile: CustomerProfile) -> list[str]:
    """Return unique locations in the order they first appeared."""
    locations = []

    for transaction in profile.historical_transactions:
        if transaction.location is not None and transaction.location not in locations:
            locations.append(transaction.location)

    return locations


def calculate_typical_transaction_hours(profile: CustomerProfile) -> list[int]:
    """Return unique transaction hours in the order they first appeared."""
    hours = []

    for transaction in profile.historical_transactions:
        if transaction.timestamp is not None:
            hour = transaction.timestamp.hour
            if hour not in hours:
                hours.append(hour)

    return hours

def build_profile_summary(profile: CustomerProfile) -> ProfileSummary:
    """Build a profile summary from a customer's historical transactions."""
    return ProfileSummary(
        customer_id=profile.customer_id,
        typical_amount=calculate_typical_amount(profile),
        common_merchants=calculate_common_merchants(profile),
        typical_locations=calculate_typical_locations(profile),
        typical_transaction_hours=calculate_typical_transaction_hours(profile),
    )