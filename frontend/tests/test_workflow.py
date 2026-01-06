import pytest
from unittest.mock import patch, MagicMock
import requests
import api_client

# --- Test 1: Interface Workflow (Create -> List) ---
def test_streamlit_workflow_create_creature_then_visible_in_registry():
    """
    Simulate the workflow:
    1. User (via UI code) calls create_creature
    2. User (via UI code) calls get_creatures
    3. Verify the new creature is present
    """
    
    # Mock data
    new_creature = {
        "id": 1,
        "name": "Workflow Dragon",
        "creature_type": "Draconic", 
        "mythology": "Test",
        "danger_level": 10
    }
    
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        # Setup Mocks
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = new_creature
        
        # First get might be empty
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [new_creature]

        # 1. Simulate Creation (Action)
        payload = {"name": "Workflow Dragon", "creature_type": "Draconic"}
        result_create = api_client.create_creature(payload)
        
        # 2. Simulate Refresh/List (Observation)
        result_list = api_client.get_creatures()
        
        # 3. Verification
        assert result_create["name"] == "Workflow Dragon"
        assert len(result_list) == 1
        assert result_list[0]["name"] == "Workflow Dragon"

# --- Test 2: Error Handling (Backend Unavailable) ---
def test_streamlit_backend_unreachable_shows_friendly_error_and_no_crash():
    """
    Verify that if the backend is down, the app handles it gracefully 
    (returns empty list instead of crashing).
    """
    with patch("requests.get") as mock_get:
        # Simulate connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        # Call the function used by the UI
        creatures = api_client.get_creatures()
        classes = api_client.get_classes()
        
        # Assertions
        # Should return empty lists, not raise exception
        assert creatures == []
        assert classes == []

# --- Test 3: Extra Feature (Summary Metric) ---
def test_summary_metric_matches_backend_count():
    """
    Verify that the metric logic (count of creatures) matches the data from backend.
    """
    mock_data = [
        {"id": 1, "name": "A", "danger_level": 5},
        {"id": 2, "name": "B", "danger_level": 5},
        {"id": 3, "name": "C", "danger_level": 5},
    ]
    
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_data
        
        # Fetch data
        creatures = api_client.get_creatures()
        
        # Calculate metric (as dashboard.py does)
        total_count = len(creatures)
        
        # Verify
        assert total_count == 3
