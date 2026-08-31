from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.category import CategoryDB
from backend.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> CategoryDB:
    """
    Create a new category in the database.

    Args:
        category (CategoryCreate): The category data to create.
        db (Session): The database session.
    Returns:
        CategoryDB: The created category object.
    """
    db_category = CategoryDB(
        name=category.name,
        type=category.type,
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),  # noqa: B008
) -> list[CategoryDB]:
    """
    Retrieve all categories from the database.

    Args:
        db (Session): The database session.
    Returns:
        list[CategoryDB]: A list of all category objects.
    """
    return list(db.scalars(select(CategoryDB)).all())
