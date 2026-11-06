from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_employee_list():
    response = client.get("/employees")
    assert response.status_code == 200


def test_employee_found(monkeypatch):
    monkeypatch.setattr(
        "src.main.employees",
        [{"name": "Karthi", "salary": 50000}]
    )
    response = client.get("/employees/Karthi")
    assert response.status_code == 200


def test_employee_not_found(monkeypatch):
    monkeypatch.setattr("src.main.employees", [])
    response = client.get("/employees/Ravi")
    assert response.status_code == 404


def test_invalid_salary():
    response = client.post(
        "/employees",
        json={"name": "Ravi", "salary": -5}
    )
    assert response.status_code == 422


def test_empty_name():
    response = client.post(
        "/employees",
        json={"name": "", "salary": 50000}
    )
    assert response.status_code == 422
