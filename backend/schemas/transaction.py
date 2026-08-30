from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    amount: Decimal
    currency: str = "EUR"
    date: date
    description: str | None = None
    type: str
    account_id: int
    category_id: int


class TransactionResponse(TransactionCreate):
    id: int
    