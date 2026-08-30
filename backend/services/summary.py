from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from backend.models.transaction import TransactionDB
from backend.schemas.enums import TransactionType
from backend.schemas.summary import CashFlowSummary


def get_cash_flow_summary(
    db: Session,
    start_date: date,
    end_date: date,
) -> CashFlowSummary:
    """
    Calculate the cash flow summary for a given date range.

    Args:
        db (Session): The database session.
        start_date (date): The start date for the summary.
        end_date (date): The end date for the summary.

    Returns:
        CashFlowSummary: The calculated cash flow summary.
    """
    transactions = (
        db.query(TransactionDB)
        .filter(
            TransactionDB.date >= start_date,
            TransactionDB.date <= end_date,
        )
        .all()
    )

    income = sum(
        (
            transaction.amount
            for transaction in transactions
            if transaction.type == TransactionType.INCOME
        ),
        Decimal("0"),
    )

    expenses = sum(
        (
            transaction.amount
            for transaction in transactions
            if transaction.type == TransactionType.EXPENSE
        ),
        Decimal("0"),
    )

    return CashFlowSummary(
        income=income,
        expenses=expenses,
        net_cash_flow=income - expenses,
    )
