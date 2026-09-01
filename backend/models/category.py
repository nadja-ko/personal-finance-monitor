from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.connection import Base

if TYPE_CHECKING:
    from backend.models.transaction import TransactionDB


class CategoryDB(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(20))

    # True: default category, cannot be deleted, False: user-defined category
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Defines the relationship with the TransactionDB model
    transactions: Mapped[list["TransactionDB"]] = relationship(
        back_populates="category"
    )

    # Self-referential hierarchy
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )

    # remote_side shows that table points at itself
    parent: Mapped["CategoryDB | None"] = relationship(
        "CategoryDB", remote_side=[id], back_populates="children"
    )

    children: Mapped[list["CategoryDB"]] = relationship(
        "CategoryDB", back_populates="parent"
    )
