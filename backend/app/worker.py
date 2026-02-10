import os
from pathlib import Path
import httpx
import base64
from arq.connections import RedisSettings
from sqlmodel import Session
import app.db as db
from app.models import Creature
from urllib.parse import urlparse

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
BASE_DIR = Path(__file__).resolve().parents[1]  # backend/
STATIC_DIR = Path(os.getenv("STATIC_DIR", BASE_DIR / "static"))
CREATURES_DIR = Path(os.getenv("CREATURES_DIR", STATIC_DIR / "creatures"))

engine = db.engine

parsed = urlparse(REDIS_URL)
host = parsed.hostname or "localhost"
port = parsed.port or 6379
password = parsed.password
database = 0
try:
    if parsed.path and len(parsed.path) > 1:
        database = int(parsed.path[1:])
except Exception:
    pass


async def startup(ctx):
    print("Worker starting...")
    # Verify database engine connection.


async def shutdown(ctx):
    print("Worker shutting down...")


async def generate_creature_image(ctx, creature_id: int, request_id: str | None = None):
    print(f"Generating image for creature {creature_id} (ReqID: {request_id})")
    with Session(engine) as session:
        creature = session.get(Creature, creature_id)
        if not creature:
            print(f"Creature {creature_id} not found.")
            return

        # Idempotency check
        if creature.image_status == "ready" and creature.image_url:
            # Check for existing image file.
            if os.path.exists(f"/app{creature.image_url}"):
                print(f"Creature {creature_id} already has image. Skipping.")
                return

        ai_url = os.getenv("AI_SERVICE_URL", "http://ai-service:8000")

        # Construct visual tokens for the image generation prompt.
        visual_tokens = (
            f"{creature.creature_type} {creature.mythology} {creature.habitat}"
        )

        prompt = (
            f"High-end fantasy creature concept art, bright neutral studio background with soft gradient, no vignette, "
            f"centered composition, clean silhouette, ultra-detailed textures, soft key light and gentle fill light, "
            f"balanced exposure, lifted shadows, soft glow accents, sharp focus, shallow depth of field, "
            f"clean color grading, vibrant but natural colors, 4k digital painting, "
            f"no text, no watermark, no logo. "
            f"Creature: {creature.name}. Class: {creature.creature_type}. "
            f"Mythology: {creature.mythology}. Habitat: {creature.habitat}. "
            f"Visual design cues: {visual_tokens}. "
            f"Full body (or portrait if specified), 3/4 view, subject fills ~70% of frame, minimal background, "
            f"a few floating particles/sparks, strong readable shapes, consistent style. "
            f"Negative: No text, no captions, no UI, no frame, no border, no extra characters, no gore, no nudity, "
            f"no photorealistic camera look, no low-res, no blurry, no distorted anatomy, no duplicate heads/limbs, "
            f"no underexposure, no heavy shadows, no dark scene."
        )

        print(f"Prompt Length: {len(prompt)}", flush=True)
        print(f"Prompt Start: {prompt[:300]}", flush=True)

        headers = {}
        if request_id:
            headers["X-Request-ID"] = request_id

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Use v1 endpoint as per requirements.
                resp = await client.post(
                    f"{ai_url}/v1/generate_image",
                    json={"prompt": prompt},
                    headers=headers,
                )
                resp.raise_for_status()
                data = resp.json()

            image_b64 = data.get("image_base64")
            if not image_b64:
                raise ValueError("No image_base64 in response")

            # Save file
            CREATURES_DIR.mkdir(parents=True, exist_ok=True)
            filename = f"{creature_id}.png"
            file_path = CREATURES_DIR / filename

            with open(file_path, "wb") as f:
                f.write(base64.b64decode(image_b64))

            # Update DB
            creature.image_url = f"/static/creatures/{filename}"
            creature.image_status = "ready"
            creature.image_error = None
            session.add(creature)
            session.commit()
            print(f"Image generated for {creature_id} at {creature.image_url}")

        except Exception as e:
            print(f"Failed to generate image for {creature_id}: {e}")
            creature.image_status = "failed"
            creature.image_error = str(e)
            session.add(creature)
            session.commit()
            raise e  # Trigger retry mechanism


class WorkerSettings:
    functions = [generate_creature_image]
    redis_settings = RedisSettings(
        host=host, port=port, password=password, database=database
    )
    on_startup = startup
    on_shutdown = shutdown
