from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from backend.models.account import AccountDB
from backend.models.category import CategoryDB
from backend.models.transaction import TransactionDB
from backend.models.trips import TripDB
from backend.schemas.enums import CashFlowType
from backend.schemas.transaction import TransactionCreate


def test_transaction_amount_must_be_positive() -> None:
    """Tests that creating a transaction at API boundary with a negative
    amount raises a ValidationError. Pydantic schema."""

    with pytest.raises(ValidationError):
        TransactionCreate(
            amount=Decimal("-10.00"),
            currency="EUR",
            date=date(2026, 8, 30),
            description="invalid expense",
            type=CashFlowType.EXPENSE,
            account_id=1,
            category_id=1,
        )


def test_transaction_amount_cannot_be_zero() -> None:
    """Tests that creating a transaction at API boundary with a zero
    amount raises a ValidationError. Pydantic schema."""

    with pytest.raises(ValidationError):
        TransactionCreate(
            amount=Decimal("0.00"),
            currency="EUR",
            date=date(2026, 8, 30),
            description="zero transaction",
            type=CashFlowType.EXPENSE,
            account_id=1,
            category_id=1,
        )


def test_valid_transaction() -> None:
    """Tests that creating a valid transaction at API boundary does not
    raise a ValidationError. Pydantic schema."""

    transaction = TransactionCreate(
        amount=Decimal("47.50"),
        currency="EUR",
        date=date(2026, 8, 30),
        description="weekly groceries",
        type=CashFlowType.EXPENSE,
        account_id=1,
        category_id=1,
    )

    assert transaction.amount == Decimal("47.50")
    assert transaction.type == CashFlowType.EXPENSE
    assert transaction.currency == "EUR"


def test_transaction_relationships(
    db_session, test_account: AccountDB, test_category: CategoryDB, test_trip: TripDB
) -> None:
    """Tests that transactions are properly related to
    their associated accounts and categories."""

    transaction = TransactionDB(
        amount=Decimal("50.00"),
        currency="EUR",
        date=date(2026, 8, 31),
        description="groceries",
        type=CashFlowType.EXPENSE,
        account_id=test_account.id,
        category_id=test_category.id,
        trip_id=test_trip.id,
    )

    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    assert transaction.account == test_account
    assert transaction.category == test_category
    assert transaction.trip == test_trip

    assert test_account.transactions == [transaction]
    assert test_category.transactions == [transaction]
    assert test_trip.transactions == [transaction]
