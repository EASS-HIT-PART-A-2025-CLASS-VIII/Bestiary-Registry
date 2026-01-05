from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models import Creature, CreatureCreate


def create_creature(session: Session, creature: CreatureCreate) -> Creature:
    # Auto-generate AI Avatar URL if not provided
    if not creature.image_url:
        from urllib.parse import quote

        # Use DiceBear Identicon as the standard avatar generator
        safe_name = quote(creature.name)
        creature.image_url = (
            f"https://api.dicebear.com/7.x/identicon/svg?seed={safe_name}"
        )

    # Auto-stamp
    creature.last_modify = datetime.now(timezone.utc).isoformat()

    # --- AUTO-REGISTER CLASS ---
    # If the creature_type is not in CreatureClass table, add it.
    from app.models import CreatureClass

    existing_class = session.exec(
        select(CreatureClass).where(CreatureClass.name == creature.creature_type)
    ).first()
    if not existing_class:
        # Default "Other" styling
        new_class = CreatureClass(
            name=creature.creature_type,
            color="rgba(127,19,236,0.1)",
            border_color="rgba(127,19,236,0.2)",
            text_color="#ad92c9",
        )
        session.add(new_class)
        # We don't need to refresh new_class here as long as it's committed with the creature

    db_creature = Creature.model_validate(creature)
    session.add(db_creature)
    session.commit()
    session.refresh(db_creature)
    return db_creature


def list_creatures(session: Session) -> list[Creature]:
    creatures = session.exec(select(Creature)).all()
    return creatures


def update_creature(
    session: Session, creature_id: int, creature: CreatureCreate
) -> Creature:
    db_creature = session.get(Creature, creature_id)
    if not db_creature:
        raise HTTPException(status_code=404, detail="Creature not found")

    creature_data = creature.model_dump(exclude_unset=True)
    for key, value in creature_data.items():
        setattr(db_creature, key, value)

    # Update timestamp
    db_creature.last_modify = datetime.now(timezone.utc).isoformat()

    session.add(db_creature)
    session.commit()
    session.refresh(db_creature)
    return db_creature


def delete_creature(session: Session, creature_id: int) -> None:
    db_creature = session.get(Creature, creature_id)
    if not db_creature:
        raise HTTPException(status_code=404, detail="Creature not found")

    session.delete(db_creature)
    session.commit()
