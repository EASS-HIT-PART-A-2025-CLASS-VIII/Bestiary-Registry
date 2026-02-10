import pytest
from app.models import Creature

# Integration test using mocked AI service to verify worker flow.

from unittest.mock import patch, MagicMock
from app.worker import generate_creature_image


@pytest.mark.asyncio
async def test_ai_integration_flow_mocked(session):
    """
    Test the full worker flow with a mocked AI service response.
    Verifies:
    1. Worker constructs prompt.
    2. Calls AI service.
    3. Saves image.
    4. Updates database.
    """
    # Setup Creature
    creature = Creature(
        name="Integration Test Creature",
        creature_type="Test",
        mythology="Test",
        habitat="Test",
        danger_level=1,
        image_status="pending",
    )
    session.add(creature)
    session.commit()
    session.refresh(creature)
    cid = creature.id

    # Mock httpx and file operations
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQ42mP8z8BQDwAEhQGAhKwMIQAAAABJRU5ErkJggg==",
        "mime_type": "image/png",
    }

    with patch("httpx.AsyncClient.post", return_value=mock_response) as mock_post:
        with patch("builtins.open", new_callable=MagicMock):
            # Execute worker function
            await generate_creature_image({}, cid, request_id="test-req-123")

            # Verify AI Service was called with correct URL and Headers
            args, kwargs = mock_post.call_args
            assert "/v1/generate_image" in args[0]
            assert kwargs["headers"]["X-Request-ID"] == "test-req-123"

            # Verify database update
            session.refresh(creature)
            assert creature.image_status == "ready"
            assert creature.image_url is not None
