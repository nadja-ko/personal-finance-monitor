from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.account import AccountDB
from backend.schemas.account import AccountCreate, AccountResponse

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/", response_model=AccountResponse)
def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db), # noqa: B008
) -> AccountDB:
    """
    Function writes accounts information into database.

    Args:
        account (AccountCreate): Account information to be stored in the database.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        AccountDB: The newly created account object from the database.
    """
    db_account = AccountDB(
        name=account.name,
        bank=account.bank,
        currency=account.currency,
        account_type=account.account_type,
    )

    # Add the new account to the database
    db.add(db_account)
    # Commit the transaction to save the changes permanently in the database
    db.commit()
    # Refresh the instance to reflect the changes made in the database,
    # returning db-generated id
    db.refresh(db_account)

    return db_account


@router.get("/", response_model=list[AccountResponse])
def get_accounts(db: Session = Depends(get_db), # noqa: B008
    ) -> list[AccountDB]:
    """
    Function retrieves all accounts from the database.

    Args:
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        list[AccountDB]: A list of all account objects from the database.
    """
    return db.query(AccountDB).all()
