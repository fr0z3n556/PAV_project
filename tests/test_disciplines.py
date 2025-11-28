from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import admin_required
from app.models.user import Users

client = TestClient(app)

# Mock для обхода авторизации в тестах
def override_admin_required():
    return Users(id=1, username="test_admin", password="test", role="admin")

app.dependency_overrides[admin_required] = override_admin_required

def test_create_discipline():
    # Arrange
    new_discipline = {"code": "MATH101", "name": "Математика", "theoretical_hours": 30, "practical_hours": 10, "self_work_hours": 20, "course_project_hours": 10, "semester": 1}

    # Act
    response = client.post("/api/v1/disciplines", json=new_discipline)

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "Математика"
    print("Тест на создание дисциплин пройден успешно!")
    
