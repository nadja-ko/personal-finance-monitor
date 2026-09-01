from sqlalchemy.orm import Session

from backend.models.account import AccountDB
from backend.models.category import CategoryDB
from backend.models.transaction import TransactionDB
from backend.schemas.transaction import TransactionCreate


def create_transaction(
    transaction: TransactionCreate,
    db: Session,
) -> TransactionDB:
    """
    Create a new transaction in the database.

    Args:
        transaction (TransactionCreate): The transaction data to be created.
        db (Session): The database session dependency.
    Returns:
        TransactionDB: The created transaction object from the database.
    """

    # Check if the account exists in the database
    account = db.get(AccountDB, transaction.account_id)

    if account is None:
        raise ValueError("Account not found")

    # Check if the category exists in the database
    category = db.get(CategoryDB, transaction.category_id)

    if category is None:
        raise ValueError("Category not found")

    if category.type != transaction.type:
        raise ValueError(
            "Transaction type must match category type",
        )

    # Create a new TransactionDB object and add it to the database
    db_transaction = TransactionDB(
        amount=transaction.amount,
        currency=transaction.currency,
        date=transaction.date,
        description=transaction.description,
        type=transaction.type,
        account_id=transaction.account_id,
        category_id=transaction.category_id,
        trip_id=transaction.trip_id,
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction
