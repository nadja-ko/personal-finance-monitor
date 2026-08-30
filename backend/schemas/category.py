from pydantic import BaseModel

from backend.schemas.enums import TransactionType


class CategoryCreate(BaseModel):
    name: str
    type: TransactionType


class CategoryResponse(CategoryCreate):
    id: int
