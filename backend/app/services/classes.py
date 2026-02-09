from sqlmodel import Session, select
from fastapi import HTTPException
from app.models import (
    CreatureClass,
    CreatureClassCreate,
    CreatureClassUpdate,
    Creature,
)


def create_class(session: Session, class_data: CreatureClassCreate) -> CreatureClass:
    # Ensure class name is unique.
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


def list_classes(session: Session) -> list[CreatureClass]:
    return session.exec(select(CreatureClass)).all()


def delete_class(session: Session, class_id: int):
    class_item = session.get(CreatureClass, class_id)
    if not class_item:
        raise HTTPException(status_code=404, detail="Class not found")
    session.delete(class_item)
    session.commit()


def update_class(
    session: Session, class_id: int, class_update: CreatureClassUpdate
) -> CreatureClass:
    db_class = session.get(CreatureClass, class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail="Class not found")

    old_name = db_class.name
    update_data = class_update.model_dump(exclude_unset=True)

    # Detect name change.
    new_name = update_data.get("name")
    name_changed = new_name and new_name != old_name

    for key, value in update_data.items():
        setattr(db_class, key, value)

    session.add(db_class)

    # Propagate name change to associated creatures.
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
