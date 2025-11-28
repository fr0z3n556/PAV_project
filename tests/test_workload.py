from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import admin_required
from app.models.user import Users

client = TestClient(app)

# Mock для обхода авторизации в тестах
def override_admin_required():
    return Users(id=1, username="test_admin", password="test", role="admin")

app.dependency_overrides[admin_required] = override_admin_required

def test_create_workload():
    # Arrange
    new_workload = {"teacher_id": 1, "discipline_id": 1, "hours": 40, "semester": 1}

    # Act
    response = client.post("/api/v1/workloads", json=new_workload)

    # Assert
    assert response.status_code == 200
    assert response.json()["hours"] == 40
    print("Тест на создание нагрузки пройден успешно!")

