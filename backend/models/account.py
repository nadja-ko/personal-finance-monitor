from pydantic import BaseModel


class Account(BaseModel):
    id: int
    name: str
    bank: str
    currency: str = "EUR"
    account_type: str