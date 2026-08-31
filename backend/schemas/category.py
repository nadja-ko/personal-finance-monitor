from pydantic import BaseModel

from backend.schemas.enums import CashFlowType


class CategoryCreate(BaseModel):
    name: str
    type: CashFlowType


class CategoryResponse(CategoryCreate):
    id: int
