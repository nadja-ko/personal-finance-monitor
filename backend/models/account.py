from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.connection import Base

if TYPE_CHECKING:
    from backend.models.transaction import TransactionDB


class AccountDB(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    bank: Mapped[str] = mapped_column(String(100))
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    account_type: Mapped[str] = mapped_column(String(50))
    # Remark: TransactionDB not imported here, as accounts aleady
    # imported in transaction.py, which would cause a circular import error
    # --> it is a forward reference
    transactions: Mapped[list["TransactionDB"]] = relationship(back_populates="account")
