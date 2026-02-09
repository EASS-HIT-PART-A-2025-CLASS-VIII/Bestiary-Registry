import pytest
import os
from unittest.mock import AsyncMock, patch
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient

# Ensure models are registered for metadata creation.
from app import models  # noqa: F401

# 2. Force SQLite for tests unless overridden (and handle engine patching)
os.environ.setdefault("DATABASE_URL", "sqlite://")

# Import app modules after environment configuration.
from app.app import app
from app.db import get_session


@pytest.fixture(name="engine")
def engine_fixture():
    """
    Create a shared in-memory SQLite engine.
    Use StaticPool so all connections are the same (sharing state between test and app).
    """
    # Use in-memory SQLite for isolation and speed.
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(autouse=True)
def patch_engines(engine):
    """
    Patch app engines ONLY when using sqlite.
    If DATABASE_URL points to Postgres, do not patch so tests can hit the real DB.
    """
    db_url = os.environ.get("DATABASE_URL", "sqlite://")
    if db_url.startswith("postgresql"):
        yield
        return

    with patch("app.db.engine", engine), patch("app.worker.engine", engine):
        yield


@pytest.fixture(autouse=True)
def mock_redis():
    """
    Mock Redis connection pool to prevent external connections during tests.
    """
    mock_pool = AsyncMock()
    mock_pool.enqueue_job.return_value = None
    mock_pool.close.return_value = None

    with patch("arq.create_pool", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = mock_pool
        yield mock_create


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()
