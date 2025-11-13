from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_teacher():
    # Arrange
    new_teacher = {"first_name": "John", "last_name": "Doe", "patronymic": "Smith", "photo": "teacher_photo.jpg"}

    # Act
    response = client.post("/api/v1/teachers", json=new_teacher)

    # Assert
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
