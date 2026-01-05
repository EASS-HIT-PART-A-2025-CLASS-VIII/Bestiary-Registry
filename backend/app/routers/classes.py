from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.db import SessionDep
from app.models import (
    CreatureClass,
    CreatureClassCreate,
    CreatureClassRead,
    CreatureClassUpdate,
    Creature,
)

router = APIRouter(prefix="/classes", tags=["classes"])


@router.post("/", response_model=CreatureClassRead)
def create_class(class_data: CreatureClassCreate, session: SessionDep):
    # Check uniqueness
    existing = session.exec(
        select(CreatureClass).where(CreatureClass.name == class_data.name)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Class already exists")

    db_class = CreatureClass.model_validate(class_data)
    session.add(db_class)
    session.commit()
    session.refresh(db_class)
    return db_class


@router.get("/", response_model=list[CreatureClassRead])
def read_classes(session: SessionDep):
    return session.exec(select(CreatureClass)).all()


@router.delete("/{class_id}")
def delete_class(class_id: int, session: SessionDep):
    class_item = session.get(CreatureClass, class_id)
    if not class_item:
        raise HTTPException(status_code=404, detail="Class not found")
    session.delete(class_item)
    session.commit()
    return {"ok": True}


@router.put("/{class_id}", response_model=CreatureClassRead)
def update_class(class_id: int, class_update: CreatureClassUpdate, session: SessionDep):
    db_class = session.get(CreatureClass, class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")

    old_name = db_class.name
    update_data = class_update.dict(exclude_unset=True)

    # Check if name is changing
    new_name = update_data.get("name")
    name_changed = new_name and new_name != old_name

    for key, value in update_data.items():
        setattr(db_class, key, value)

    session.add(db_class)

    # Cascade update if name changed
    if name_changed:
        creatures = session.exec(
            select(Creature).where(Creature.creature_type == old_name)
        ).all()
        for c in creatures:
            c.creature_type = new_name
            session.add(c)

    session.commit()
    session.refresh(db_class)
    return db_class
