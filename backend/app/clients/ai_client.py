import os
import httpx
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class AiClient:
    def __init__(self, base_url: Optional[str] = None, timeout: float = 5.0):
        self.base_url = base_url or os.getenv(
            "AI_SERVICE_URL", "http://ai-service:8000"
        )
        self.timeout = timeout

    def generate_avatar(self, name: str) -> str:
        """
        Calls the AI service to generate an avatar URL for the given name.
        Returns a fallback URL if the service is unreachable or errors.
        """
        url = f"{self.base_url}/generate_avatar"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json={"name": name})
                response.raise_for_status()
                data = response.json()
                return data.get("url")
        except httpx.RequestError as exc:
            logger.error(
                f"An error occurred while requesting {exc.request.url!r}: {exc}"
            )
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )
        except Exception as e:
            logger.error(f"Unexpected error calling AI service: {e}")

        # Fallback if service fails (so we don't break the user flow entirely,
        # though functionally we might want to raise an error depending on strictness.
        # Requirement says "handle connection errors / 5xx properly", "normalize errors returned to frontend".
        # Returning a default/fallback seems safe for 'avatar'.
        from urllib.parse import quote

        safe_name = quote(name)
        return f"https://api.dicebear.com/7.x/identicon/svg?seed={safe_name}&scale=80"
