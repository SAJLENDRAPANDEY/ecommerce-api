from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def get_auth_token():
    email = "producttest@example.com"

    register_response = client.post(
        "/auth/register",
        json={
            "name": "Product Test User",
            "email": email,
            "password": "test12345"
        }
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "test12345"
        }
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_product_not_found():
    response = client.get("/products/999999")
    assert response.status_code == 404


def test_create_product():
    token = get_auth_token()

    response = client.post(
        "/products/",
        json={
            "name": "Test Laptop",
            "description": "Test laptop for API testing",
            "price": 50000,
            "stock": 10
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Laptop"
    assert data["price"] == 50000
    assert data["stock"] == 10