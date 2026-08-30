from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.connection import Base


class Account(BaseModel):
    id: int
    name: str
    bank: str
    currency: str = "EUR"
    account_type: str


class AccountDB(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    bank: Mapped[str] = mapped_column(String(100))
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    account_type: Mapped[str] = mapped_column(String(50))
