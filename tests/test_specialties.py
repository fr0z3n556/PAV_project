from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_specialty():
    # Arrange
    new_specialty = {"code": "CS101", "name": "Computer Science"}

    # Act
    response = client.post("/api/v1/specialties", json=new_specialty)

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "Computer Science"
    print("Тест на создание специальности пройден успешно!")
