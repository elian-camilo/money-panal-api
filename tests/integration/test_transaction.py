def test_create_transaction(client, seed_db):
    # Act
    payload = {
        "amount": 15000,
        "t_type": "expense",
        "description": "Test Transaction",
        "category_id": 1,
        "account_id": 1,
        "user_id": 1
    }
    response = client.post("/api/v1/transactions/", json=payload)
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 15000
    assert data["description"] == "Test Transaction"
    assert "category_id" in data

def test_get_transactions(client, seed_db):
    # Arrange
    payload = {
        "amount": 15000,
        "t_type": "expense",
        "description": "Test Transaction",
        "category_id": 1,
        "account_id": 1,
        "user_id": 1
    }
    client.post("/api/v1/transactions/", json=payload)
    
    # Act
    response = client.get("/api/v1/transactions/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["description"] == "Test Transaction"
    assert data[0]["amount"] == 15000

def test_get_transaction_by_id(client, seed_db):
    # Arrange
    payload = {
        "amount": 15000,
        "t_type": "expense",
        "description": "Test Transaction",
        "category_id": 1,
        "account_id": 1,
        "user_id": 1
    }
    create_response = client.post("/api/v1/transactions/", json=payload)
    transaction_id = create_response.json()["id"]
    
    # Act
    response = client.get(f"/api/v1/transactions/{transaction_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction_id
    assert data["description"] == "Test Transaction"
    assert data["amount"] == 15000

def test_update_transaction(client, seed_db):
    # Arrange
    payload = {
        "amount": 15000,
        "t_type": "expense",
        "description": "Test Transaction",
        "category_id": 1,
        "account_id": 1,
        "user_id": 1
    }
    create_response = client.post("/api/v1/transactions/", json=payload)
    transaction_id = create_response.json()["id"]
    
    update_payload = {
        "amount": 20000,
        "t_type": "income",
        "description": "Updated Transaction",
        "category_id": 1,
        "account_id": 1,
        "user_id": 1
    }
    
    # Act
    response = client.put(f"/api/v1/transactions/{transaction_id}", json=update_payload)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction_id
    assert data["description"] == "Updated Transaction"
    assert data["amount"] == 20000
    assert data["t_type"] == "income"

def test_delete_transaction(client, seed_db):
    # Arrange
    payload = {
        "amount": 15000,
        "t_type": "expense",
        "description": "Test Transaction",
        "category_id": 1,
        "account_id": 1,
        "user_id": 1
    }
    create_response = client.post("/api/v1/transactions/", json=payload)
    transaction_id = create_response.json()["id"]
    
    # Act
    response = client.delete(f"/api/v1/transactions/{transaction_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

    # Verify deletion
    get_response = client.get(f"/api/v1/transactions/{transaction_id}")
    assert get_response.status_code == 404