from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import urllib.parse
import os
import io
import base64
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MOCK_MODE = os.getenv("MOCK_MODE", "0").lower() in ["1", "true"]
logger.info(f"MOCK_MODE is: {MOCK_MODE} (Raw: {os.getenv('MOCK_MODE')})")
GEMINI_MODEL_ID = os.getenv("GEMINI_MODEL_ID", "imagen-4.0-generate-001")


class AvatarRequest(BaseModel):
    name: str


class ImagePrompt(BaseModel):
    prompt: str


# Compatibility alias.
class ImageRequest(BaseModel):
    prompt: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate_avatar")
def generate_avatar(request: AvatarRequest):
    safe_name = urllib.parse.quote(request.name)
    url = f"https://api.dicebear.com/7.x/identicon/svg?seed={safe_name}"
    return {"url": url}


@app.post("/v1/generate_image")
async def generate_image(request: ImagePrompt, http_req: Request):
    req_id = http_req.headers.get("X-Request-ID", "N/A")
    logger.info(
        f"[{req_id}] Received image generation request. Prompt length: {len(request.prompt)}"
    )

    # Mock response handling.
    if MOCK_MODE:
        logger.info(f"[{req_id}] Mock mode active. Returning placeholder image.")
        dummy_img = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQ42mP8z8BQDwAEhQGAhKwMIQAAAABJRU5ErkJggg=="
        return {"image_base64": dummy_img, "mime_type": "image/png"}

    # Configuration validation.
    if not GEMINI_API_KEY:
        logger.error(f"[{req_id}] GEMINI_API_KEY is not set")
        raise HTTPException(
            status_code=500, detail="Server configuration error: Missing API Key"
        )

    # Dynamic imports.
    try:
        from google import genai
        from google.genai import types
    except ImportError as e:
        logger.error(f"[{req_id}] Missing dependencies: {e}")
        raise HTTPException(
            status_code=500, detail="Server misconfiguration: Missing libraries"
        )

    # Execute Gemini generation.
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info(f"[{req_id}] Calling Gemini model: {GEMINI_MODEL_ID}")

        response = client.models.generate_images(
            model=GEMINI_MODEL_ID,
            prompt=request.prompt,
            config=types.GenerateImagesConfig(number_of_images=1),
        )
    except Exception as e:
        logger.exception(f"[{req_id}] Gemini call failed")
        raise HTTPException(status_code=502, detail=str(e))

    # Extract image from response.
    img_obj = None
    if hasattr(response, "generated_images") and response.generated_images:
        img_obj = response.generated_images[0].image

    if img_obj is None:
        logger.error(f"[{req_id}] Gemini returned no image object")
        raise HTTPException(status_code=502, detail="Gemini returned no image object")

    # Convert image to bytes.
    image_bytes = None

    try:
        # Case 1: raw bytes
        if isinstance(img_obj, (bytes, bytearray)):
            image_bytes = bytes(img_obj)

        # Case 2: BytesIO
        elif isinstance(img_obj, io.BytesIO):
            image_bytes = img_obj.getvalue()

        # Case 3: PIL Image or object with save()
        elif hasattr(img_obj, "save"):
            buffered = io.BytesIO()
            try:
                # Attempt save to buffer.
                img_obj.save(buffered, format="PNG")
                image_bytes = buffered.getvalue()
            except TypeError:
                # Fallback to temporary file save.
                import tempfile
                from pathlib import Path

                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                    tmp_path = tmp.name

                try:
                    img_obj.save(tmp_path)
                    image_bytes = Path(tmp_path).read_bytes()
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
        else:
            raise ValueError(f"Unsupported image type: {type(img_obj)}")

    except Exception:
        logger.exception(f"[{req_id}] Failed to process image object: {type(img_obj)}")
        raise HTTPException(status_code=502, detail="Failed to process generated image")

    if not image_bytes:
        logger.error(f"[{req_id}] No image bytes produced")
        raise HTTPException(status_code=502, detail="Failed to produce image bytes")

    b64_str = base64.b64encode(image_bytes).decode("utf-8")
    logger.info(f"[{req_id}] Image generated successfully")
    return {"image_base64": b64_str, "mime_type": "image/png"}
