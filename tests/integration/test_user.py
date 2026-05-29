def test_register_user(client):
    # Act
    payload = {
        "first_name": "Lionel",
        "last_name": "Messi",
        "email": "messi10@barca.com",
        "password": "secret_password"
    }
    response = client.post("/api/v1/users/", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["first_name"] == "Lionel"
    assert data["last_name"] == "Messi"
    assert data["email"] == "messi10@barca.com"


def test_get_own_user_profile(client, seed_db):
    # Act: current_user.id is mocked to 1 in override_get_current_user
    response = client.get("/api/v1/users/1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["email"] == "test@test.com"


def test_get_other_user_profile_returns_unauthorized(client, seed_db):
    # Act: current_user.id is mocked to 1, we request ID 2
    response = client.get("/api/v1/users/2")

    # Assert
    assert response.status_code == 401
    assert response.json()["message"] == "You don't have access to this resource."


def test_list_users_returns_unauthorized(client, seed_db):
    # Act
    response = client.get("/api/v1/users/")

    # Assert
    assert response.status_code == 401
    assert response.json()["message"] == "You don't have permission to list users."


def test_update_own_user_profile(client, seed_db):
    # Arrange
    payload = {
        "first_name": "Test Updated",
        "last_name": "User Updated",
        "email": "test@test.com",
        "password": "testing_password"
    }

    # Act
    response = client.put("/api/v1/users/1", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Test Updated"
    assert data["last_name"] == "User Updated"


def test_update_other_user_profile_returns_unauthorized(client, seed_db):
    # Arrange
    payload = {
        "first_name": "Test Updated",
        "last_name": "User Updated",
        "email": "test@test.com",
        "password": "testing_password"
    }

    # Act
    response = client.put("/api/v1/users/2", json=payload)

    # Assert
    assert response.status_code == 401
    assert response.json()["message"] == "You don't have access to this resource."


def test_delete_own_user_profile(client, session):
    from app.presentation.api.dependencies import get_current_user
    from app.domain.entities.user import User
    from app.infraestructure.models.user import UserTable
    from app.main import app

    # Create a fresh user with id=2 in database that has no foreign key references
    fresh_user_db = UserTable(
        id=2,
        first_name="Fresh",
        last_name="User",
        email="fresh@user.com",
        password="password"
    )
    session.add(fresh_user_db)
    session.commit()

    # Override get_current_user to return this fresh user (id=2)
    app.dependency_overrides[get_current_user] = lambda: User(
        id=2,
        first_name="Fresh",
        last_name="User",
        email="fresh@user.com",
        password="password"
    )

    try:
        # Act
        response = client.delete("/api/v1/users/2")

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "status": "success",
            "message": "User deleted successfully",
            "deleted_id": 2
        }
    finally:
        # Restore default override
        app.dependency_overrides[get_current_user] = lambda: User(
            id=1,
            first_name="Test",
            last_name="User",
            email="test@test.com",
            password="testing_password"
        )


def test_delete_other_user_profile_returns_unauthorized(client, seed_db):
    # Act: current_user.id is mocked to 1, we try to delete ID 2
    response = client.delete("/api/v1/users/2")

    # Assert
    assert response.status_code == 401
    assert response.json()["message"] == "You don't have access to this resource."
