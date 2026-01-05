import requests
import time

API_URL = "http://localhost:8000"


def test_backend():
    print("--- Starting Backend Tests ---")

    # 1. Test Creating Creature with New Class
    print("\n1. Testing Auto-Creation of New Class...")
    new_class_name = f"TestClass_{int(time.time())}"
    creature_name = f"TestCreature_{int(time.time())}"

    payload = {
        "name": creature_name,
        "creature_type": new_class_name,
        "mythology": "TestMyth",
        "danger_level": 5,
        "habitat": "TestHabitat",
    }

    res = requests.post(f"{API_URL}/creatures/", json=payload)
    if res.status_code != 200:
        print(f"FAILED to create creature: {res.text}")
        return

    creature_id = res.json()["id"]
    print(f"Creature created (ID: {creature_id}, Type: {new_class_name})")

    # Check if class exists
    res = requests.get(f"{API_URL}/classes/")
    classes = res.json()
    class_found = next((c for c in classes if c["name"] == new_class_name), None)

    if class_found:
        print(
            f"SUCCESS: Class '{new_class_name}' was auto-created (ID: {class_found['id']})"
        )
    else:
        print(f"FAILED: Class '{new_class_name}' was NOT found in /classes/ list.")
        return

    # 2. Test Cascading Update
    print("\n2. Testing Cascading Update (Rename Class)...")
    class_id = class_found["id"]
    renamed_class_name = f"{new_class_name}_RENAMED"

    update_payload = {"name": renamed_class_name}
    res = requests.put(f"{API_URL}/classes/{class_id}", json=update_payload)

    if res.status_code != 200:
        print(f"FAILED to update class: {res.text}")
        return

    print(f"Class renamed to '{renamed_class_name}'")

    # Check if creature updated
    res = requests.get(f"{API_URL}/creatures/")
    creatures = res.json()
    creature = next((c for c in creatures if c["id"] == creature_id), None)

    if creature and creature["creature_type"] == renamed_class_name:
        print(f"SUCCESS: Creature type updated to '{renamed_class_name}'")
    else:
        actual_type = creature["creature_type"] if creature else "None"
        print(
            f"FAILED: Creature type is '{actual_type}', expected '{renamed_class_name}'"
        )

    # Clean up
    # requests.delete(f"{API_URL}/creatures/{creature_id}")
    # requests.delete(f"{API_URL}/classes/{class_id}")


if __name__ == "__main__":
    test_backend()
