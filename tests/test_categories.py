from fastapi.testclient import TestClient

from backend.models.category import CategoryDB
from backend.schemas.enums import CashFlowType


def test_create_category(client: TestClient) -> None:
    """Test that a category can be created successfully."""
    response = client.post(
        "/categories/",
        json={
            "name": "salary",
            "type": CashFlowType.INCOME,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "salary"
    assert data["type"] == CashFlowType.INCOME


def test_create_expense_category(client: TestClient) -> None:
    """Test that an expense category can be created successfully."""
    response = client.post(
        "/categories/",
        json={
            "name": "groceries",
            "type": CashFlowType.EXPENSE,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "groceries"
    assert data["type"] == CashFlowType.EXPENSE


def test_get_categories(client: TestClient) -> None:
    client.post(
        "/categories/",
        json={
            "name": "salary",
            "type": CashFlowType.INCOME,
        },
    )

    client.post(
        "/categories/",
        json={
            "name": "groceries",
            "type": CashFlowType.EXPENSE,
        },
    )

    response = client.get("/categories/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]["name"] == "salary"
    assert data[0]["type"] == CashFlowType.INCOME

    assert data[1]["name"] == "groceries"
    assert data[1]["type"] == CashFlowType.EXPENSE


def test_get_categories_returns_empty_list(client: TestClient) -> None:
    """Test that getting categories returns an empty list when no categories exist."""
    response = client.get("/categories/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_category_rejects_invalid_type(client: TestClient) -> None:
    """Test that creating a category with an invalid type is rejected."""
    response = client.post(
        "/categories/",
        json={
            "name": "salary",
            "type": "invalid",
        },
    )

    assert response.status_code == 422


def test_category_parent_child_relationship(db_session):
    """ Test that a category can have a parent and child relationship. """

    # parent category with parent_id set to None
    food = CategoryDB(
        name="food",
        type=CashFlowType.EXPENSE,
    )

    db_session.add(food)
    db_session.commit()
    db_session.refresh(food)

    # child category with parent_id set to the id of its parent `food`
    groceries = CategoryDB(
        name="groceries",
        type=CashFlowType.EXPENSE,
        parent_id=food.id,
    )

    db_session.add(groceries)
    db_session.commit()
    db_session.refresh(groceries)

    assert groceries.parent == food
    assert food.children == [groceries]
    