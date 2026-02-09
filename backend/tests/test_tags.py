from fastapi.testclient import TestClient

# Test using in-memory database for isolation.


def test_tags_flow(client: TestClient):
    # 1. Create Tag
    response = client.post("/tags", json={"name": "Fire"})
    assert response.status_code == 200
    assert response.json()["name"] == "Fire"

    # 2. Create Creature
    client.post(
        "/creatures/",
        json={
            "name": "Dragon",
            "mythology": "European",
            "creature_type": "Beast",
            "danger_level": 5,
            "habitat": "Cave",
        },
    )

    # 3. Add Tag to Creature
    response = client.post("/creatures/Dragon/tags/Fire")
    assert response.status_code == 200
    assert response.json()["status"] == "tagged"

    # Verify tagging status (implicit check via response status).

    # Test duplicate tag
    response = client.post("/creatures/Dragon/tags/Fire")
    assert response.status_code == 200
    assert response.json()["status"] == "already tagged"
