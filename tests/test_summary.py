from datetime import date
from decimal import Decimal

from fastapi.testclient import TestClient

from backend.models.account import AccountDB
from backend.models.category import CategoryDB
from backend.models.transaction import TransactionDB
from backend.schemas.enums import CashFlowType
from backend.services.summary import get_cash_flow_summary


def test_cash_flow_summary(db_session) -> None:

    db_session.add(
        AccountDB(
            name="test account",
            bank="test bank",
            currency="EUR",
            account_type="checking",
        )
    )

    db_session.add(
        CategoryDB(
            name="income",
            type=CashFlowType.INCOME,
            parent_id=1
        )
    )

    db_session.commit()

    transactions = [
        TransactionDB(
            amount=Decimal("2500.00"),
            currency="EUR",
            date=date(2026, 8, 1),
            description="salary",
            type=CashFlowType.INCOME,
            account_id=1,
            category_id=1,
        ),
        TransactionDB(
            amount=Decimal("50.00"),
            currency="EUR",
            date=date(2026, 8, 5),
            description="groceries",
            type=CashFlowType.EXPENSE,
            account_id=1,
            category_id=2,
        ),
        TransactionDB(
            amount=Decimal("800.00"),
            currency="EUR",
            date=date(2026, 8, 10),
            description="Rent",
            type=CashFlowType.EXPENSE,
            account_id=1,
            category_id=2,
        ),
    ]

    db_session.add_all(transactions)
    db_session.commit()

    summary = get_cash_flow_summary(
        db=db_session,
        start_date=date(2026, 8, 1),
        end_date=date(2026, 8, 31),
    )

    assert summary.income == Decimal("2500.00")
    assert summary.expenses == Decimal("850.00")
    assert summary.net_cash_flow == Decimal("1650.00")


def test_cash_flow_summary_api(client: TestClient, db_session) -> None:
    db_session.add(
        AccountDB(
            name="test account",
            bank="test bank",
            currency="EUR",
            account_type="checking",
        )
    )

    db_session.add(
        CategoryDB(
            name="income",
            type=CashFlowType.INCOME,
            parent_id=1
        )
    )

    db_session.add(
        CategoryDB(
            name="expenses",
            type=CashFlowType.EXPENSE,
            parent_id=1
        )
    )

    db_session.commit()

    transactions = [
        TransactionDB(
            amount=Decimal("2500.00"),
            currency="EUR",
            date=date(2026, 8, 1),
            description="salary",
            type=CashFlowType.INCOME,
            account_id=1,
            category_id=1,
        ),
        TransactionDB(
            amount=Decimal("50.00"),
            currency="EUR",
            date=date(2026, 8, 5),
            description="groceries",
            type=CashFlowType.EXPENSE,
            account_id=1,
            category_id=2,
        ),
        TransactionDB(
            amount=Decimal("800.00"),
            currency="EUR",
            date=date(2026, 8, 10),
            description="rent",
            type=CashFlowType.EXPENSE,
            account_id=1,
            category_id=2,
        ),
    ]

    db_session.add_all(transactions)
    db_session.commit()

    response = client.get(
        "/summary/cash-flow",
        params={
            "start_date": "2026-08-01",
            "end_date": "2026-08-31",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["income"] == "2500.00"
    assert data["expenses"] == "850.00"
    assert data["net_cash_flow"] == "1650.00"
