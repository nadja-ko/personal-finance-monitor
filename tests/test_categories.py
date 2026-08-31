from fastapi.testclient import TestClient


def test_create_category(client: TestClient) -> None:
    response = client.post(
        "/categories/",
        json={
            "name": "salary",
            "type": "income",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "salary"
    assert data["type"] == "income"


def test_create_expense_category(client: TestClient) -> None:
    response = client.post(
        "/categories/",
        json={
            "name": "groceries",
            "type": "expense",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "groceries"
    assert data["type"] == "expense"


def test_get_categories(client: TestClient) -> None:
    client.post(
        "/categories/",
        json={
            "name": "salary",
            "type": "income",
        },
    )

    client.post(
        "/categories/",
        json={
            "name": "groceries",
            "type": "expense",
        },
    )

    response = client.get("/categories/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]["name"] == "salary"
    assert data[0]["type"] == "income"

    assert data[1]["name"] == "groceries"
    assert data[1]["type"] == "expense"


def test_get_categories_returns_empty_list(client: TestClient) -> None:
    response = client.get("/categories/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_category_rejects_invalid_type(client: TestClient) -> None:
    response = client.post(
        "/categories/",
        json={
            "name": "salary",
            "type": "invalid",
        },
    )

    assert response.status_code == 422
