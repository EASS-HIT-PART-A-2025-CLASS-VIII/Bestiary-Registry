from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import create_db_and_tables  # get_session re-exported for tests
from app.routers import creatures, classes


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(creatures.router)
app.include_router(classes.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "creatures-backend"}
