from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import admin_required
from app.models.user import Users

client = TestClient(app)

# Mock для обхода авторизации в тестах
def override_admin_required():
    return Users(id=1, username="test_admin", password="test", role="admin")

app.dependency_overrides[admin_required] = override_admin_required

def test_create_teacher():
    # Arrange
    new_teacher = {"first_name": "Иван", "last_name": "Иванов", "patronymic": "Иванович", "photo": "teacher_photo.jpg"}

    # Act
    response = client.post("/api/v1/teachers", json=new_teacher)

    # Assert
    assert response.status_code == 200
    assert response.json()["first_name"] == "Иван"
    print("Тест на создание педагога пройден успешно!")
