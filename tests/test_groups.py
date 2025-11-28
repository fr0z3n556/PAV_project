from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import admin_required
from app.models.user import Users

client = TestClient(app)

# Mock для обхода авторизации в тестах
def override_admin_required():
    return Users(id=1, username="test_admin", password="test", role="admin")

app.dependency_overrides[admin_required] = override_admin_required

def test_create_group():
    # Arrange
    new_group = {"group_number": "31", "specialty_id": 1, "form": "очно", "group_type": "бюджет"}

    # Act
    response = client.post("/api/v1/groups", json=new_group)

    # Assert
    assert response.status_code == 200
    assert response.json()["group_number"] == "31"
    print("Тест на создание групп пройден успешно!")
     