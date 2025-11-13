from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_workload():
    # Arrange
    new_workload = {"teacher_id": 1, "discipline_id": 1, "hours": 40, "semester": 1}

    # Act
    response = client.post("/api/v1/workload", json=new_workload)

    # Assert
    assert response.status_code == 200
    assert response.json()["hours"] == 40
