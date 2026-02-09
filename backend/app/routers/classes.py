from fastapi import APIRouter
from app.db import SessionDep
from app.models import (
    CreatureClassCreate,
    CreatureClassRead,
    CreatureClassUpdate,
)
from app.services import classes as service

router = APIRouter(prefix="/classes", tags=["classes"])


@router.post("/", response_model=CreatureClassRead)
def create_class(class_data: CreatureClassCreate, session: SessionDep):
    """Create a new creature class."""
    return service.create_class(session, class_data)


@router.get("/", response_model=list[CreatureClassRead])
def read_classes(session: SessionDep):
    """List all available creature classes."""
    return service.list_classes(session)


@router.delete("/{class_id}")
def delete_class(class_id: int, session: SessionDep):
    """Delete a creature class."""
    service.delete_class(session, class_id)
    return {"ok": True}


@router.put("/{class_id}", response_model=CreatureClassRead)
def update_class(class_id: int, class_update: CreatureClassUpdate, session: SessionDep):
    """Update a creature class."""
    return service.update_class(session, class_id, class_update)
