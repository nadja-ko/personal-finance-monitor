def test_create_trip(client):
    """Test creating a new trip in the database."""
    response = client.post(
        "/trips/",
        json={
            "name": "Peru 2026",
            "start_date": "2026-09-01",
            "end_date": "2026-10-15",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Peru 2026"
    assert data["start_date"] == "2026-09-01"
    assert data["end_date"] == "2026-10-15"
    assert "id" in data


def test_get_trips(client):
    """Test retrieving trips from the database."""
    client.post(
        "/trips/",
        json={
            "name": "Peru 2026",
            "start_date": "2026-09-01",
            "end_date": "2026-10-15",
        },
    )

    client.post(
        "/trips/",
        json={
            "name": "Portugal 2027",
            "start_date": "2027-05-01",
        },
    )

    response = client.get("/trips/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Peru 2026"
    assert data[1]["name"] == "Portugal 2027"
