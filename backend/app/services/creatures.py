from fastapi import HTTPException
from sqlmodel import Session, select
from app.models import Creature, CreatureCreate


def create_creature(session: Session, creature: CreatureCreate) -> Creature:
    # Auto-generate AI Avatar URL if not provided
    if not creature.image_url:
        from urllib.parse import quote

        # Switch to Robohash (set2 = monsters) because Pollinations.ai is currently down
        safe_name = quote(creature.name)
        creature.image_url = f"https://robohash.org/{safe_name}?set=set2&size=200x200"

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
