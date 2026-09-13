from transaction_agent import (
    Evidence,
    EvidenceDirection,
    Transaction,
    ProfileSummary,
    VerificationResponse,
)


def check_amount_evidence(
    transaction: Transaction,
    profile_summary: ProfileSummary,
) -> Evidence:
    if transaction.amount is None or profile_summary.typical_amount is None:
        return Evidence(
            name="amount_unknown",
            direction=EvidenceDirection.NEUTRAL,
        )

    if transaction.amount > profile_summary.typical_amount * 1.5:
        return Evidence(
            name="large_amount",
            direction=EvidenceDirection.SUPPORTS_FRAUDULENT,
        )

    return Evidence(
        name="amount_consistent",
        direction=EvidenceDirection.SUPPORTS_LEGITIMATE,
    )


def check_merchant_evidence(
    transaction: Transaction,
    profile_summary: ProfileSummary,
) -> Evidence:
    if transaction.merchant is None:
        return Evidence(
            name="merchant_unknown",
            direction=EvidenceDirection.NEUTRAL,
        )

    if transaction.merchant not in profile_summary.common_merchants:
        return Evidence(
            name="new_merchant",
            direction=EvidenceDirection.SUPPORTS_FRAUDULENT,
        )

    return Evidence(
        name="merchant_consistent",
        direction=EvidenceDirection.SUPPORTS_LEGITIMATE,
    )


def check_location_evidence(
    transaction: Transaction,
    profile_summary: ProfileSummary,
) -> Evidence:
    if transaction.location is None:
        return Evidence(
            name="location_unknown",
            direction=EvidenceDirection.NEUTRAL,
        )

    if transaction.location not in profile_summary.typical_locations:
        return Evidence(
            name="unusual_location",
            direction=EvidenceDirection.SUPPORTS_FRAUDULENT,
        )

    return Evidence(
        name="location_consistent",
        direction=EvidenceDirection.SUPPORTS_LEGITIMATE,
    )


def check_time_evidence(
    transaction: Transaction,
    profile_summary: ProfileSummary,
) -> Evidence:
    if transaction.timestamp is None:
        return Evidence(
            name="time_unknown",
            direction=EvidenceDirection.NEUTRAL,
        )

    if transaction.timestamp.hour not in profile_summary.typical_transaction_hours:
        return Evidence(
            name="unusual_time",
            direction=EvidenceDirection.SUPPORTS_FRAUDULENT,
        )

    return Evidence(
        name="time_consistent",
        direction=EvidenceDirection.SUPPORTS_LEGITIMATE,
    )


def extract_evidence(
    transaction: Transaction,
    profile_summary: ProfileSummary,
) -> list[Evidence]:
    return [
        check_amount_evidence(transaction, profile_summary),
        check_merchant_evidence(transaction, profile_summary),
        check_location_evidence(transaction, profile_summary),
        check_time_evidence(transaction, profile_summary),
    ]

def extract_verification_evidence(verification):
    if verification.response == VerificationResponse.CONFIRMED:
        return Evidence(
            name="customer_confirms",
            direction=EvidenceDirection.SUPPORTS_LEGITIMATE,
        )

    if verification.response == VerificationResponse.DENIED:
        return Evidence(
            name="customer_denies",
            direction=EvidenceDirection.SUPPORTS_FRAUDULENT,
        )

    return Evidence(
        name="verification_unknown",
        direction=EvidenceDirection.NEUTRAL,
    )
