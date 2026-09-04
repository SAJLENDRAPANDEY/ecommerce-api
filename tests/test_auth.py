from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "test12345"
        }
    )

    assert response.status_code in [201, 409]


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "Healthy"