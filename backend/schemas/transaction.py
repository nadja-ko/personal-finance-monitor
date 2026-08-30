from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from backend.schemas.enums import TransactionType


class TransactionCreate(BaseModel):
    amount: Decimal = Field(
        gt=0, description="The amount of the transaction. Must be greater than 0."
    )
    currency: str = "EUR"
    date: date
    description: str | None = None
    type: TransactionType
    account_id: int
    category_id: int


class TransactionResponse(TransactionCreate):
    id: int
