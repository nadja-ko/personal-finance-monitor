from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from backend.schemas.transaction import TransactionCreate


def test_transaction_amount_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        TransactionCreate(
            amount=Decimal("-10.00"),
            currency="EUR",
            date=date(2026, 8, 30),
            description="Invalid expense",
            type="expense",
            account_id=1,
            category_id=1,
        )


def test_transaction_amount_cannot_be_zero() -> None:
    with pytest.raises(ValidationError):
        TransactionCreate(
            amount=Decimal("0.00"),
            currency="EUR",
            date=date(2026, 8, 30),
            description="Zero transaction",
            type="expense",
            account_id=1,
            category_id=1,
        )


def test_valid_transaction() -> None:
    transaction = TransactionCreate(
        amount=Decimal("47.50"),
        currency="EUR",
        date=date(2026, 8, 30),
        description="Weekly groceries",
        type="expense",
        account_id=1,
        category_id=1,
    )

    assert transaction.amount == Decimal("47.50")
    assert transaction.type == "expense"
    assert transaction.currency == "EUR"
