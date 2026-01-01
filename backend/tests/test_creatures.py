import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.app import app, get_session

# 1. Setup In-Memory Database for Testing
# poolclass=StaticPool is CRITICAL. It ensures the in-memory DB persists
# across multiple threads (which TestClient might simulate).
engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)


@pytest.fixture(name="session")
def session_fixture():
    # Setup: Create tables
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Teardown: Drop tables to ensure clean state for next test
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    # 2. Override Dependency
    # We use 'return' (not yield) because the 'session' fixture above
    # already handles the lifecycle (open/close). The override just passes it through.
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()


# 3. Tests


def test_create_creature(client: TestClient):
    payload = {
        "name": "Test Dragon",
        "mythology": "Norse",
        "creature_type": "Reptile",
        "danger_level": 9,
        "habitat": "Mountains",
    }
    response = client.post("/creatures/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data
    # Verify the AI avatar logic ran (Robohash default)
    assert "robohash.org" in data["image_url"]


def test_get_creatures(client: TestClient):
    # Seed the DB
    payload = {
        "name": "Unicorn",
        "mythology": "Greek",
        "creature_type": "Equine",
        "danger_level": 1,
    }
    client.post("/creatures/", json=payload)

    response = client.get("/creatures/")
    assert response.status_code == 200
    data = response.json()

    # Verification: List ordering is not guaranteed by SQL without ORDER BY.
    # We check if the item exists in the returned list, rather than checking index 0.
    names = [c["name"] for c in data]
    assert "Unicorn" in names


def test_update_creature(client: TestClient):
    # Setup
    create_res = client.post(
        "/creatures/",
        json={
            "name": "Base Creature",
            "mythology": "Test",
            "creature_type": "Test",
            "danger_level": 5,
        },
    )
    creature_id = create_res.json()["id"]

    # Update
    payload = {
        "name": "Evolved Creature",
        "mythology": "Test",
        "creature_type": "God",
        "danger_level": 10,
    }
    response = client.put(f"/creatures/{creature_id}", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Evolved Creature"
    assert data["danger_level"] == 10


def test_delete_creature(client: TestClient):
    # Setup
    create_res = client.post(
        "/creatures/",
        json={
            "name": "To Delete",
            "mythology": "Test",
            "creature_type": "Test",
            "danger_level": 1,
        },
    )
    creature_id = create_res.json()["id"]

    # Delete
    response = client.delete(f"/creatures/{creature_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "creature deleted successfully"}

    # Verify Gone
    get_res = client.get("/creatures/")
    current_ids = [c["id"] for c in get_res.json()]
    assert creature_id not in current_ids
