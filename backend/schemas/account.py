from pydantic import BaseModel


class AccountCreate(BaseModel):
    name: str
    bank: str
    currency: str = "EUR"
    account_type: str


class AccountResponse(AccountCreate):
    id: int
