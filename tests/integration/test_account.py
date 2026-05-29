def test_create_account(client, seed_db):
    # Act
    payload = {
        "name": "Savings Account",
        "amount": 250000.0,
        "profit_percentage": 2.5,
        "currency": "cop"
    }
    response = client.post("/api/v1/accounts/", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Savings Account"
    assert data["amount"] == 250000.0
    assert data["profit_percentage"] == 2.5
    assert data["currency"] == "cop"
    assert data["user_id"] == 1
    assert "created_at" in data


def test_get_accounts(client, seed_db):
    # Arrange
    payload = {
        "name": "Investment Fund",
        "amount": 500000.0,
        "profit_percentage": 5.0,
        "currency": "usd"
    }
    client.post("/api/v1/accounts/", json=payload)

    # Act
    response = client.get("/api/v1/accounts/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Seeded db already has one Account Table with id=1
    assert data[0]["name"] == "Test Account"
    assert "user_id" in data[0]


def test_get_account_by_id(client, seed_db):
    # Act
    response = client.get("/api/v1/accounts/1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Account"
    assert data["user_id"] == 1


def test_update_account(client, seed_db):
    # Arrange
    update_payload = {
        "name": "Updated Account Name",
        "amount": 99999.0,
        "profit_percentage": 1.2,
        "currency": "cad"
    }

    # Act
    response = client.put("/api/v1/accounts/1", json=update_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Updated Account Name"
    assert data["amount"] == 99999.0
    assert data["profit_percentage"] == 1.2
    assert data["currency"] == "cad"
    assert data["user_id"] == 1


def test_delete_account(client, seed_db):
    # Act
    response = client.delete("/api/v1/accounts/1")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Account deleted successfully",
        "deleted_id": 1
    }

    # Verify deletion
    get_response = client.get("/api/v1/accounts/1")
    assert get_response.status_code == 404
