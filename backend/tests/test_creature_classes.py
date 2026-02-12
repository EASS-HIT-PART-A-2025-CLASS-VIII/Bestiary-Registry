import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.app import app
from app.db import get_session
from app.models import Creature

# Database Validation Fixtures
engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()


# Happy Path Tests


def test_create_class(client: TestClient):
    payload = {"name": "Test Class", "color": "#123456", "text_color": "#ffffff"}
    response = client.post("/classes/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Class"
    assert "id" in data


def test_create_duplicate_class(client: TestClient):
    payload = {"name": "Unique Class", "color": "#000", "text_color": "#fff"}
    client.post("/classes/", json=payload)
    response = client.post("/classes/", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Class already exists"


def test_update_class_rename_cascade(client: TestClient, session: Session):
    # 1. Create Class
    c_res = client.post(
        "/classes/", json={"name": "Old Name", "color": "#000", "text_color": "#fff"}
    )
    class_id = c_res.json()["id"]

    # 2. Create Creature of that class
    creature = Creature(
        name="Beast",
        creature_type="Old Name",
        mythology="Test",
        danger_level=5,
        habitat="Cave",
    )
    session.add(creature)
    session.commit()

    # 3. Rename Class
    res = client.put(f"/classes/{class_id}", json={"name": "New Name"})
    assert res.status_code == 200
    assert res.json()["name"] == "New Name"

    # 4. Verify Cascade
    session.refresh(creature)
    assert creature.creature_type == "New Name"


def test_delete_class(client: TestClient):
    c_res = client.post(
        "/classes/", json={"name": "To Delete", "color": "#000", "text_color": "#fff"}
    )
    class_id = c_res.json()["id"]

    res = client.delete(f"/classes/{class_id}")
    assert res.status_code == 204


# Error Handling Tests (404)


def test_delete_class_not_found(client: TestClient):
    response = client.delete("/classes/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Class not found"


def test_update_class_not_found(client: TestClient):
    payload = {"name": "Ghost Class"}
    response = client.put("/classes/99999", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Class not found"


# Validation Tests (422)


def test_create_class_missing_name(client: TestClient):
    # Missing 'name'
    payload = {"color": "#000", "text_color": "#fff"}
    response = client.post("/classes/", json=payload)
    assert response.status_code == 422
