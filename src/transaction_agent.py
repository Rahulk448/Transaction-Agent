"""Importable Transaction Agent domain model module."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class HiddenState(str, Enum):
    """Possible true transaction states that are not directly observed."""

    LEGITIMATE = "legitimate"
    FRAUDULENT = "fraudulent"


class Action(str, Enum):
    """Actions available to the transaction decision agent."""

    APPROVE = "approve"
    HOLD = "hold"
    STOP = "stop"


class EvidenceDirection(str, Enum):
    """How an evidence signal points relative to the hidden state."""

    SUPPORTS_LEGITIMATE = "supports_legitimate"
    SUPPORTS_FRAUDULENT = "supports_fraudulent"
    NEUTRAL = "neutral"


class VerificationResponse(str, Enum):
    """Customer verification response values."""

    CONFIRMED = "confirmed"
    DENIED = "denied"
    NO_RESPONSE = "no_response"
    UNKNOWN = "unknown"


@dataclass
class Transaction:
    """An observed financial transaction."""

    transaction_id: str
    customer_id: str
    amount: float | None = None
    merchant: str | None = None
    timestamp: datetime | None = None
    location: str | None = None


@dataclass
class HistoricalTransaction:
    """A historical transaction used to understand customer behavior."""

    transaction_id: str
    customer_id: str
    amount: float | None = None
    merchant: str | None = None
    timestamp: datetime | None = None
    location: str | None = None


@dataclass
class CustomerProfile:
    """Historical information used to understand customer behavior."""

    customer_id: str
    historical_transactions: list[HistoricalTransaction]


@dataclass
class Evidence:
    """An observed signal relevant to the transaction decision."""

    name: str
    direction: EvidenceDirection


@dataclass
class Belief:
    """Current probability belief over the hidden transaction states."""

    legitimate_probability: float
    fraudulent_probability: float


@dataclass
class CostModel:
    """Costs associated with actions under each hidden transaction state."""

    approve_legitimate: float
    approve_fraudulent: float
    hold_legitimate: float
    hold_fraudulent: float
    stop_legitimate: float
    stop_fraudulent: float


@dataclass
class Decision:
    """A decision made by the transaction decision agent."""

    action: Action
    expected_cost: float


@dataclass
class Verification:
    """Customer verification information."""

    response: VerificationResponse


@dataclass
class PendingVerification:
    """A transaction awaiting customer verification."""

    transaction_id: str


__all__: list[str] = [
    "Action",
    "Belief",
    "CostModel",
    "CustomerProfile",
    "Decision",
    "Evidence",
    "EvidenceDirection",
    "HiddenState",
    "HistoricalTransaction",
    "PendingVerification",
    "Transaction",
    "Verification",
    "VerificationResponse",
]