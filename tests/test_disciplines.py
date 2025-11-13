from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_discipline():
    # Arrange
    new_discipline = {"code": "MATH101", "name": "Mathematics", "theoretical_hours": 30, "practical_hours": 10, "self_work_hours": 20, "course_project_hours": 10, "semester": 1}

    # Act
    response = client.post("/api/v1/disciplines", json=new_discipline)

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "Mathematics"