from datetime import date as date_type
from typing import TYPE_CHECKING

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.connection import Base

if TYPE_CHECKING:
    from backend.models.transaction import TransactionDB


class TripDB(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    start_date: Mapped[date_type] = mapped_column(Date)
    end_date: Mapped[date_type | None] = mapped_column(Date, nullable=True)

    transactions: Mapped[list["TransactionDB"]] = relationship(back_populates="trip")
