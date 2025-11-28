from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import admin_required
from app.models.user import Users

client = TestClient(app)

# Mock для обхода авторизации в тестах
def override_admin_required():
    return Users(id=1, username="test_admin", password="test", role="admin")

app.dependency_overrides[admin_required] = override_admin_required

def test_create_specialty():
    # Arrange
    new_specialty = {"code": "ИП", "name": "Информационные системы"}

    # Act
    response = client.post("/api/v1/specialties", json=new_specialty)

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "Информационные системы"
    print("Тест на создание специальности пройден успешно!")

