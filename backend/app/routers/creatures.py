from fastapi import APIRouter
from app.models import CreatureCreate, CreatureRead
from app.db import SessionDep
from app.services import creatures as service

router = APIRouter(prefix="/creatures", tags=["creatures"])


@router.post("/", response_model=CreatureRead)
async def create_creature_endpoint(
    creature: CreatureCreate, session: SessionDep
) -> CreatureRead:
    """Create a new creature and enqueue image generation."""
    return await service.create_creature(session, creature)


@router.get("/", response_model=list[CreatureRead])
def get_creatures_endpoint(session: SessionDep) -> list[CreatureRead]:
    """List all creatures."""
    return service.list_creatures(session)


@router.get("/{creature_id}", response_model=CreatureRead)
def get_creature_endpoint(creature_id: int, session: SessionDep) -> CreatureRead:
    """Retrieve a specific creature by ID."""
    return service.get_creature(session, creature_id)


@router.put("/{creature_id}", response_model=CreatureRead)
def update_creature_endpoint(
    creature_id: int, creature: CreatureCreate, session: SessionDep
) -> CreatureRead:
    """Update a creature's details."""
    return service.update_creature(session, creature_id, creature)


@router.delete("/{creature_id}")
def delete_creature_endpoint(creature_id: int, session: SessionDep) -> dict:
    """Delete a creature."""
    service.delete_creature(session, creature_id)
    return {"detail": "creature deleted successfully"}
