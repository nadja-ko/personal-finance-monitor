from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    type: str


class CategoryResponse(CategoryCreate):
    id: int
