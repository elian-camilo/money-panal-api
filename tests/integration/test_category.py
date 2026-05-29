def test_create_category(client, seed_db):
    # Act
    payload = {
        "name": "Entertainment",
        "description": "Movies and games"
    }
    response = client.post("/api/v1/categories/", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Entertainment"
    assert data["description"] == "Movies and games"
    assert data["user_id"] == 1
    assert "created_at" in data

def test_get_categories(client, seed_db):
    # Arrange
    payload = {
        "name": "Entertainment",
        "description": "Movies and games"
    }
    client.post("/api/v1/categories/", json=payload)

    # Act
    response = client.get("/api/v1/categories/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Test Category"
    assert "user_id" in data[0]

def test_get_category_by_id(client, seed_db):
    # Act
    response = client.get("/api/v1/categories/1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Category"
    assert data["user_id"] == 1

def test_update_category(client, seed_db):
    # Arrange
    update_payload = {
        "name": "Updated Category",
        "description": "Updated Description"
    }

    # Act
    response = client.put("/api/v1/categories/1", json=update_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Updated Category"
    assert data["description"] == "Updated Description"
    assert data["user_id"] == 1

def test_delete_category(client, seed_db):
    # Act
    response = client.delete("/api/v1/categories/1")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Category deleted successfully",
        "delete_id": 1
    }

    # Verify deletion
    get_response = client.get("/api/v1/categories/1")
    assert get_response.status_code == 404
