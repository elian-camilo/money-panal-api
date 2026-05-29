def test_create_obligation(client, seed_db):
    # Act
    payload = {
        "name": "Water Bill",
        "description": "Monthly water service",
        "amount": 45.0,
        "due_date": "2027-12-31",
        "is_paid": False,
        "recurring": False
    }
    response = client.post("/api/v1/obligations/", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Water Bill"
    assert data["amount"] == 45.0
    assert data["due_date"] == "2027-12-31"
    assert data["user_id"] == 1
    assert "created_at" in data


def test_get_obligations(client, seed_db):
    # Arrange
    payload = {
        "name": "Internet Subscription",
        "amount": 60.0,
        "due_date": "2027-12-31",
        "is_paid": False,
        "recurring": True
    }
    client.post("/api/v1/obligations/", json=payload)

    # Act
    response = client.get("/api/v1/obligations/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Seeded db already has one Obligation Table with id=1
    assert data[0]["name"] == "Test Obligation"
    assert "user_id" in data[0]


def test_get_obligation_by_id(client, seed_db):
    # Act
    response = client.get("/api/v1/obligations/1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Obligation"
    assert data["user_id"] == 1


def test_update_obligation(client, seed_db):
    # Arrange
    update_payload = {
        "name": "Updated Obligation Name",
        "description": "Updated Description",
        "amount": 200.0,
        "due_date": "2027-12-31",
        "is_paid": True,
        "recurring": True
    }

    # Act
    response = client.put("/api/v1/obligations/1", json=update_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Updated Obligation Name"
    assert data["description"] == "Updated Description"
    assert data["amount"] == 200.0
    assert data["due_date"] == "2027-12-31"
    assert data["is_paid"] is True
    assert data["recurring"] is True
    assert data["user_id"] == 1


def test_delete_obligation(client, seed_db):
    # Act
    response = client.delete("/api/v1/obligations/1")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Obligation deleted successfully",
        "deleted_id": 1
    }

    # Verify deletion
    get_response = client.get("/api/v1/obligations/1")
    assert get_response.status_code == 404
