from fastapi import APIRouter, Path
from app.models import CreatureCreate, CreatureRead
from app.db import SessionDep
from app.services import creatures as service

router = APIRouter(prefix="/creatures", tags=["creatures"])

MAX_INT32 = 2_147_483_647


@router.post(
    "/",
    response_model=CreatureRead,
    responses={
        400: {"description": "Malformed JSON body"},
        409: {"description": "Creature already exists"},
    },
)
async def create_creature_endpoint(
    creature: CreatureCreate, session: SessionDep
) -> CreatureRead:
    """Create a new creature and enqueue image generation."""
    return await service.create_creature(session, creature)


@router.get("/", response_model=list[CreatureRead])
def get_creatures_endpoint(session: SessionDep) -> list[CreatureRead]:
    """List all creatures."""
    return service.list_creatures(session)


@router.get(
    "/{creature_id}",
    response_model=CreatureRead,
    responses={404: {"description": "Creature not found"}},
)
def get_creature_endpoint(
    creature_id: int = Path(..., ge=1, le=MAX_INT32),
    session: SessionDep = ...,
) -> CreatureRead:
    """Retrieve a specific creature by ID."""
    return service.get_creature(session, creature_id)


@router.put(
    "/{creature_id}",
    response_model=CreatureRead,
    responses={404: {"description": "Creature not found"}},
)
def update_creature_endpoint(
    creature_id: int = Path(..., ge=1, le=MAX_INT32),
    creature: CreatureCreate = ...,
    session: SessionDep = ...,
) -> CreatureRead:
    return service.update_creature(session, creature_id, creature)


@router.delete(
    "/{creature_id}",
    responses={404: {"description": "Creature not found"}},
)
def delete_creature_endpoint(
    creature_id: int = Path(..., ge=1, le=MAX_INT32),
    session: SessionDep = ...,
) -> dict:
    service.delete_creature(session, creature_id)
    return {"detail": "creature deleted successfully"}
