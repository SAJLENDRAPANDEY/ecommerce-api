from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_my_orders_without_auth():
    response = client.get("/orders/")

    assert response.status_code in [401, 403]


def test_get_order_without_auth():
    response = client.get("/orders/1")

    assert response.status_code in [401, 403]


def test_checkout_without_auth():
    response = client.post("/orders/")

    assert response.status_code in [401, 403]