


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "DevOps Lab API"
    }


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


def test_create_user(client):

    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "test@example.com"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"


def test_get_users(client):

    client.post(
        "/users",
        json={
            "name": "Lorenzo",
            "email": "lorenzo@example.com"
        }
    )

    client.post(
        "/users",
        json={
            "name": "Mario",
            "email": "mario@example.com"
        }
    )

    response = client.get("/users")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]["name"] == "Lorenzo"
    assert data[0]["email"] == "lorenzo@example.com"

    assert data[1]["name"] == "Mario"
    assert data[1]["email"] == "mario@example.com"


def test_get_user(client):

    create_response = client.post(
        "/users",
        json={
            "name": "Lorenzo",
            "email": "lorenzo@example.com"
        }
    )

    assert create_response.status_code == 200

    created_user = create_response.json()

    user_id = created_user["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["name"] == "Lorenzo"
    assert data["email"] == "lorenzo@example.com"

def test_get_user_not_found(client):

    response = client.get("/users/000000000000000000000000")

    assert response.status_code == 404




def test_update_user(client):

    create_response = client.post(
        "/users",
        json={
            "name": "Lorenzo",
            "email": "lorenzo@example.com"
        }
    )

    assert create_response.status_code == 200

    created_user = create_response.json()

    user_id = created_user["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "name": "Lorenzo Updated",
            "email": "lorenzo.updated@example.com"
        }
    )

    assert update_response.status_code == 200

    updated_user = update_response.json()

    assert updated_user["id"] == user_id
    assert updated_user["name"] == "Lorenzo Updated"
    assert updated_user["email"] == "lorenzo.updated@example.com"

    get_response = client.get(f"/users/{user_id}")

    assert get_response.status_code == 200

    user_from_database = get_response.json()

    assert user_from_database["id"] == user_id
    assert user_from_database["name"] == "Lorenzo Updated"
    assert user_from_database["email"] == "lorenzo.updated@example.com"



def test_update_user_not_found(client):

    response = client.put(
        "/users/000000000000000000000000",
        json={
            "name": "Lorenzo Updated",
            "email": "lorenzo.updated@example.com"
        }
    )

    assert response.status_code == 404


def test_delete_user(client):

    create_response = client.post(
        "/users",
        json={
            "name": "Lorenzo",
            "email": "lorenzo@example.com"
        }
    )

    assert create_response.status_code == 200

    created_user = create_response.json()

    user_id = created_user["id"]

    delete_response = client.delete(f"/users/{user_id}")

    assert delete_response.status_code == 200

    get_response = client.get(f"/users/{user_id}")

    assert get_response.status_code == 404



def test_delete_user_not_found(client):
    
    response = client.delete(
        "/users/000000000000000000000000"
    )

    assert response.status_code == 404


def test_create_duplicate_user(client):

    user = {
        "name": "Lorenzo",
        "email": "lorenzo@example.com"
    }

    first_response = client.post(
        "/users",
        json=user
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/users",
        json=user
    )

    assert second_response.status_code == 409

    assert second_response.json() == {
        "detail": "User already exists"
    }



def test_create_user_invalid_email(client):

    response = client.post(
        "/users",
        json={
            "name": "Lorenzo",
            "email": "not-an-email"
        }
    )

    assert response.status_code == 422