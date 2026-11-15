from fastapi.testclient import TestClient
from app.main import app
import os

os.makedirs("data", exist_ok=True)

client = TestClient(app)

for i in range(1, 31):
    response = client.post(
        "/add",
        json={
            "num1": i * 10,
            "num2": i * 5
        }
    )
    response.raise_for_status()

print("Successfully generated 30 API records.")
