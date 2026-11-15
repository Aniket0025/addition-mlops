
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# Test 1: Normal addition
def test_addition():
    response = client.post(
        "/add",
        json={"num1": 10, "num2": 20}
    )

    assert response.status_code == 200
    assert response.json()["result"] == 30


# Test 2: Negative numbers
def test_negative_numbers():
    response = client.post(
        "/add",
        json={"num1": -10, "num2": 5}
    )

    assert response.json()["result"] == -5


# Test 3: Decimal numbers
def test_decimal_numbers():
    response = client.post(
        "/add",
        json={"num1": 2.5, "num2": 3.5}
    )

    assert response.json()["result"] == 6.0


# Test 4: Addition with zero
def test_zero():
    response = client.post(
        "/add",
        json={"num1": 10, "num2": 0}
    )

    assert response.json()["result"] == 10


# Test 5: Invalid input
def test_invalid_input():
    response = client.post(
        "/add",
        json={"num1": "hello", "num2": 20}
    )

    assert response.status_code == 422


# Test 6: Home endpoint
def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()
