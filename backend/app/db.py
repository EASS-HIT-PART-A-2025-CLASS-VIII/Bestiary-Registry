import os
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# Database setup.
# Uses `DATABASE_URL` environment variable, defaulting to SQLite for local development.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///creatures.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    # SQLite-specific configuration for thread safety.
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
