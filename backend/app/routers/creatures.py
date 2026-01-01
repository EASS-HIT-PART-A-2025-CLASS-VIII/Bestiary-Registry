from fastapi import APIRouter
from app.models import CreatureCreate, CreatureRead
from app.db import SessionDep
from app.services import creatures as service

router = APIRouter(prefix="/creatures", tags=["creatures"])


@router.post("/", response_model=CreatureRead)
def create_creature_endpoint(
    creature: CreatureCreate, session: SessionDep
) -> CreatureRead:
    return service.create_creature(session, creature)


@router.get("/", response_model=list[CreatureRead])
def get_creatures_endpoint(session: SessionDep) -> list[CreatureRead]:
    return service.list_creatures(session)


@router.put("/{creature_id}", response_model=CreatureRead)
def update_creature_endpoint(
    creature_id: int, creature: CreatureCreate, session: SessionDep
) -> CreatureRead:
    return service.update_creature(session, creature_id, creature)


@router.delete("/{creature_id}")
def delete_creature_endpoint(creature_id: int, session: SessionDep) -> dict:
    service.delete_creature(session, creature_id)
    return {"detail": "creature deleted successfully"}
