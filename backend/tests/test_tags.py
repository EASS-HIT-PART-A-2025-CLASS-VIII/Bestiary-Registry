from fastapi.testclient import TestClient

# Test using in-memory database for isolation.


def test_tags_flow(client: TestClient):
    # 1. Create Tag
    response = client.post("/tags", json={"name": "Fire"})
    assert response.status_code == 200
    assert response.json()["name"] == "Fire"

    # 1b. Duplicate tag creation should conflict
    response = client.post("/tags", json={"name": "Fire"})
    assert response.status_code == 409
    # If your API uses a different message, adjust this set accordingly
    assert response.json()["detail"] in {"Tag already exists", "tag already exists"}

    # 2. Create Creature
    c_res = client.post(
        "/creatures/",
        json={
            "name": "Dragon",
            "mythology": "European",
            "creature_type": "Beast",
            "danger_level": 5,
            "habitat": "Cave",
        },
    )
    assert c_res.status_code == 200

    # 3. Add Tag to Creature
    response = client.post("/creatures/Dragon/tags/Fire")
    assert response.status_code == 200
    assert response.json()["status"] == "tagged"

    # 4. Duplicate tagging should conflict
    response = client.post("/creatures/Dragon/tags/Fire")
    assert response.status_code == 409
    assert response.json()["detail"] in {"Already tagged", "already tagged"}
