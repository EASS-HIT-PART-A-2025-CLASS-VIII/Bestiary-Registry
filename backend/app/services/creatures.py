from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models import Creature, CreatureCreate


async def create_creature(session: Session, creature: CreatureCreate) -> Creature:
    # Initialize image generation status.
    creature.image_status = "pending"
    creature.image_url = None  # Populated by background worker.

    # Set timestamps.
    creature.last_modify = datetime.now(timezone.utc).isoformat()

    # Automatically register new creature class if missing.
    from app.models import CreatureClass

    existing_class = session.exec(
        select(CreatureClass).where(CreatureClass.name == creature.creature_type)
    ).first()
    if not existing_class:
        new_class = CreatureClass(
            name=creature.creature_type,
            color="rgba(127,19,236,0.1)",
            border_color="rgba(127,19,236,0.2)",
            text_color="#ad92c9",
        )
        session.add(new_class)

    db_creature = Creature.model_validate(creature)
    session.add(db_creature)
    session.commit()
    session.refresh(db_creature)

    # Queue image generation job.
    try:
        from arq import create_pool
        from arq.connections import RedisSettings
        import os

        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        # Parse Redis connection settings.
        from urllib.parse import urlparse

        p = urlparse(redis_url)
        settings = RedisSettings(
            host=p.hostname or "localhost",
            port=p.port or 6379,
            password=p.password,
            database=0,
        )

        # Get Request ID from Context
        from app.app import request_id_context

        req_id = request_id_context.get()

        pool = await create_pool(settings)
        await pool.enqueue_job(
            "generate_creature_image", db_creature.id, request_id=req_id
        )
        await pool.close()
    except Exception as e:
        print(f"Failed to enqueue image generation: {e}")
        # Log failure without interrupting request.

    return db_creature


def list_creatures(session: Session) -> list[Creature]:
    creatures = session.exec(select(Creature)).all()
    return creatures


def get_creature(session: Session, creature_id: int) -> Creature:
    creature = session.get(Creature, creature_id)
    if not creature:
        raise HTTPException(status_code=404, detail="Creature not found")
    return creature


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
