from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_group():
    # Arrange
    new_group = {"group_number": "A-123", "specialty_code": "CS101", "form": "full-time", "group_type": "budget"}

    # Act
    response = client.post("/api/v1/groups", json=new_group)

    # Assert
    assert response.status_code == 200
    assert response.json()["group_number"] == "A-123"
