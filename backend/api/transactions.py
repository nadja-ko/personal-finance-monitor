from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.transaction import TransactionDB
from backend.schemas.summary import CashFlowSummary
from backend.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
)
from backend.services.summary import get_cash_flow_summary
from backend.services.transactions import (
    create_transaction as create_transaction_service,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> TransactionDB:
    """
    Create a new transaction in the database.

    Args:
        transaction (TransactionCreate): The transaction data to be created.
        db (Session): The database session dependency.
    Returns:
        TransactionDB: The created transaction object from the database."""

    try:
        return create_transaction_service(transaction, db)
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error


@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),  # noqa: B008
) -> list[TransactionDB]:
    """
    Retrieve all transactions from the database.

    Args:
        db (Session): The database session dependency.
    Returns:
        list[TransactionDB]: A list of all transaction objects from the database.
    """
    return db.query(TransactionDB).all()


@router.get("/summary", response_model=CashFlowSummary)
def get_summary(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),  # noqa: B008
) -> CashFlowSummary:
    """
    Retrieve a summary of cash flow between the specified start and end dates.

    Args:
        start_date (date): The start date for the summary.
        end_date (date): The end date for the summary.
        db (Session): The database session dependency.
    Returns:
        CashFlowSummary: A summary of cash flow between the specified dates.
    """
    return get_cash_flow_summary(
        db=db,
        start_date=start_date,
        end_date=end_date,
    )
