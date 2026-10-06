from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.models.trips import TripDB


def test_create_trip(client):
    """Test creating a new trip in the database."""
    response = client.post(
        "/trips/",
        json={
            "name": "Peru 2026",
            "start_date": date(2026, 9, 1),
            "end_date": date(2026, 10, 15)
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Peru 2026"
    assert data["start_date"] == date(2026, 9, 1)
    assert data["end_date"] == date(2026, 10, 15)
    assert "id" in data


def test_get_trips(client):
    """Test retrieving trips from the database."""
    client.post(
        "/trips/",
        json={
            "name": "Peru 2026",
            "start_date": date(2026, 9, 1),
            "end_date": date(2026, 10, 15)
        },
    )

    client.post(
        "/trips/",
        json={
            "name": "Portugal 2027",
            "start_date": date(2027, 5, 1),
        },
    )

    response = client.get("/trips/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Peru 2026"
    assert data[1]["name"] == "Portugal 2027"


def test_delete_trip(client: TestClient, db_session: Session) -> None:
    """ Test that a trip can be deleted while the transaction remains. """

    trip = TripDB(
        name="Peru 2026",
        start_date=date(2026, 9, 1),
        end_date=date(2026, 10, 15),
    )

    db_session.add(trip)
    db_session.commit()
    db_session.refresh(trip)

    response = client.delete(f"/trips/{trip.id}")

    assert response.status_code == 204

    deleted_trip = db_session.get(TripDB, trip.id)

    assert deleted_trip is None
    