def test_create_debt(client, seed_db):
    # Act
    payload = {
        "person_name": "Messi",
        "amount": 100000.5,
        "type": "borrow",
        "due_date": "2027-12-31",
        "is_settled": False
    }
    response = client.post("/api/v1/debts/", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["person_name"] == "Messi"
    assert data["amount"] == 100000.5
    assert data["type"] == "borrow"
    assert data["due_date"] == "2027-12-31"
    assert data["is_settled"] == False
    assert data["user_id"] == 1
    assert "created_at" in data


def test_get_debts(client, seed_db):
    # Arrange
    payload = {
        "person_name": "Messi",
        "amount": 100000.5,
        "type": "borrow",
        "due_date": "2027-12-31",
        "is_settled": False
    }
    client.post("/api/v1/debts/", json=payload)

    # Act
    response = client.get("/api/v1/debts/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Seeded db already has one Debt Table with id=1 [0], then Messi at [1]
    assert data[0]["person_name"] == "Ronaldo"
    assert data[1]["person_name"] == "Messi"
    assert "user_id" in data[0]


def test_get_debt_by_id(client, seed_db):
    # Act
    response = client.get("/api/v1/debts/1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["person_name"] == "Ronaldo"
    assert data["user_id"] == 1


def test_update_debt(client, seed_db):
    # Arrange
    update_payload = {
        "person_name": "Updated Ronaldo",
        "amount": 75000.0,
        "type": "lend",
        "due_date": "2027-12-31",
        "is_settled": True
    }

    # Act
    response = client.put("/api/v1/debts/1", json=update_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["person_name"] == "Updated Ronaldo"
    assert data["amount"] == 75000.0
    assert data["is_settled"] is True
    assert data["user_id"] == 1


def test_delete_debt(client, seed_db):
    # Act
    response = client.delete("/api/v1/debts/1")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Debt deleted successfully",
        "delete_id": 1
    }

    # Verify deletion
    get_response = client.get("/api/v1/debts/1")
    assert get_response.status_code == 404