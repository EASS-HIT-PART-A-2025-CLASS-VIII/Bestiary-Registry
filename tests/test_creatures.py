from fastapi.testclient import TestClient
import app.app as app_module

client = TestClient(app_module.app)


# Helper function to reset the application state before each test
def reset_state():
    app_module.items_db.clear()
    app_module.counter_id = 1


# Test creating a new creature
def test_create_creature():
    reset_state()

    payload = {
        "name": "Dragon",
        "mythology": "Fantasy",
        "creature_type": "Fire",
        "danger_level": 10,
    }
    response = client.post("/creatures/", json=payload)
    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["mythology"] == payload["mythology"]
    assert data["creature_type"] == payload["creature_type"]
    assert data["danger_level"] == payload["danger_level"]


# Test retrieving the list of creatures
def test_get_creatures():
    reset_state()

    payload = {
        "name": "Dragon",
        "mythology": "Fantasy",
        "creature_type": "Fire",
        "danger_level": 10,
    }
    client.post("/creatures/", json=payload)
    response = client.get("/creatures/")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1

    creature = data[0]
    assert creature["name"] == payload["name"]
    assert creature["mythology"] == payload["mythology"]
    assert creature["creature_type"] == payload["creature_type"]
    assert creature["danger_level"] == payload["danger_level"]


# Test updating an existing creature
def test_update_creature():
    reset_state()

    payload = {
        "name": "Dragon",
        "mythology": "Fantasy",
        "creature_type": "Fire",
        "danger_level": 10,
    }
    create_response = client.post("/creatures/", json=payload)
    creature_id = create_response.json()["id"]

    update_payload = {
        "name": "Ice Dragon",
        "mythology": "Fantasy",
        "creature_type": "Ice",
        "danger_level": 8,
    }
    response = client.put(f"/creatures/{creature_id}", json=update_payload)
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == creature_id
    assert data["name"] == update_payload["name"]
    assert data["mythology"] == update_payload["mythology"]
    assert data["creature_type"] == update_payload["creature_type"]
    assert data["danger_level"] == update_payload["danger_level"]


# Test deleting a creature
def test_delete_creature():
    reset_state()

    payload = {
        "name": "Dragon",
        "mythology": "Fantasy",
        "creature_type": "Fire",
        "danger_level": 10,
    }
    create_response = client.post("/creatures/", json=payload)
    creature_id = create_response.json()["id"]

    response = client.delete(f"/creatures/{creature_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["detail"] == "creature deleted successfully"

    get_response = client.get("/creatures/")
    creatures = get_response.json()
    assert all(creature["id"] != creature_id for creature in creatures)
