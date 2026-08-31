from pydantic import BaseModel

from backend.schemas.enums import CashFlowType


class CategoryCreate(BaseModel):
    name: str
    type: CashFlowType
    parent_id : int | None = None


class CategoryResponse(CategoryCreate):
    id: int
