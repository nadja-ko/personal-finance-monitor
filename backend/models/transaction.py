from datetime import date as date_type
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.connection import Base
from backend.models.category import CategoryDB

if TYPE_CHECKING:
    from backend.models.account import AccountDB
    from backend.models.category import CategoryDB


class TransactionDB(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    date: Mapped[date_type] = mapped_column(Date)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    type: Mapped[str] = mapped_column(String(20))
    # nullable=False means transaction must belong to category and account
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    account: Mapped["AccountDB"] = relationship(back_populates="transactions")
    category: Mapped["CategoryDB"] = relationship(back_populates="transactions")
