"""Pydantic models for the application."""

import reflex as rx
from typing import Optional, List


class Transaction(rx.Base):
    """Transaction model."""
    id: str
    client_id: int
    card_id: Optional[int] = None
    date: str
    amount: float
    use_chip: Optional[str] = None
    merchant_id: Optional[int] = None
    merchant_city: Optional[str] = None
    merchant_state: Optional[str] = None
    zip: Optional[float] = None
    mcc: Optional[int] = None
    errors: Optional[str] = None
    isFraud: int


class Customer(rx.Base):
    """Customer model."""
    id: str
    transactions_count: int
    total_amount: float
    avg_amount: float = 0.0
    fraud_count: int = 0


class DataStats(rx.Base):
    """Data statistics model."""
    total_transactions: int
    fraud_rate: float
    # Add other fields as needed for specific stats


class FraudStat(rx.Base):
    """Fraud statistics model."""
    type: str
    total_count: int
    fraud_count: int
    fraud_rate: float


class DailyStat(rx.Base):
    """Daily statistics model."""
    step: str
    count: int
    total_amount: float
    fraud_count: int
    avg_amount: float = 0.0


class TypeStat(rx.Base):
    """Statistics by transaction type model."""
    type: str
    count: int
    total_amount: float
    avg_amount: float
    fraud_rate: float = 0.0
