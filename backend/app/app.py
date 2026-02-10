from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
from app.routers import creatures, classes
from fastapi.staticfiles import StaticFiles
from fastapi import Request
import uuid
from contextvars import ContextVar
import os
from app.routers import auth
from app.routers import tags
from pathlib import Path


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute database migrations.
    # In production, this may be handled by an initialization container.
    try:
        from alembic import command
        from alembic.config import Config

        alembic_cfg = Config("alembic.ini")
        # Ensure the worker has access to the database URL environment variable.
        logger.info("Running DB migrations...")
        await run_in_threadpool(lambda: command.upgrade(alembic_cfg, "head"))
        logger.info("DB migrations verified.")

        # Optional: Seed initial data if enabled.
        import os

        if os.getenv("SEED", "false").lower() == "true":
            logger.info("Seeding data...")
            from app.seed import seed_data

            await run_in_threadpool(seed_data)
            logger.info("Seeding complete.")

    except Exception as e:
        logger.error(f"Migration/Seed failed: {e}")
        # Log failure but allow startup to proceed depending on policy.

    yield


app = FastAPI(lifespan=lifespan)


request_id_context: ContextVar[str] = ContextVar("request_id", default="N/A")


@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    token = request_id_context.set(req_id)
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        return response
    except Exception:
        logger.exception(f"[{req_id}] Unhandled exception during request processing")
        raise
    finally:
        request_id_context.reset(token)


BASE_DIR = Path(__file__).resolve().parents[1]  # backend/
STATIC_DIR = Path(os.getenv("STATIC_DIR", BASE_DIR / "static"))
CREATURES_DIR = Path(os.getenv("CREATURES_DIR", STATIC_DIR / "creatures"))

CREATURES_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


app.include_router(creatures.router)
app.include_router(classes.router)
app.include_router(auth.router)
app.include_router(tags.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "creatures-backend"}


@app.get("/health")
def health():
    # Verify dependency health (e.g., database connection) in a production environment.
    return {"status": "healthy"}


@app.get("/ready")
def ready():
    return {"status": "ready"}
