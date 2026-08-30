from datetime import date
from decimal import Decimal

from pydantic import BaseModel
from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.connection import Base


class TransactionDB(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    date: Mapped[date] = mapped_column(Date)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    type: Mapped[str] = mapped_column(String(20))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))


class Transaction(BaseModel):
    id: int
    amount: Decimal
    currency: str = "EUR"
    date: date
    description: str | None = None
    type: str
    account_id: int
    category_id: int
