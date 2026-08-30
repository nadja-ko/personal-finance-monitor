from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.transaction import TransactionDB
from backend.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
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
        TransactionDB: The created transaction object from the database.
    """
    db_transaction = TransactionDB(
        amount=transaction.amount,
        currency=transaction.currency,
        date=transaction.date,
        description=transaction.description,
        type=transaction.type,
        account_id=transaction.account_id,
        category_id=transaction.category_id,
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


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
