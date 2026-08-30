from pydantic import BaseModel

from backend.schemas.enums import AccountType


class AccountCreate(BaseModel):
    name: str
    bank: str
    currency: str = "EUR"
    account_type: AccountType


class AccountResponse(AccountCreate):
    id: int
