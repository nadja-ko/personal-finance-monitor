from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.transaction import TransactionDB
from backend.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
)
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
