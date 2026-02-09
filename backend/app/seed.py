from sqlmodel import Session, select
from app.db import engine, create_db_and_tables
from app.models import Creature, CreatureClass


def seed_data():
    # Initialize database schemas.
    create_db_and_tables()

    with Session(engine) as session:
        # Seed Creature Classes
        classes = [
            {
                "name": "Dragon",
                "color": "#FF0000",
                "border_color": "#880000",
                "text_color": "#FFFFFF",
            },
            {
                "name": "Beast",
                "color": "#00FF00",
                "border_color": "#008800",
                "text_color": "#000000",
            },
            {
                "name": "Undead",
                "color": "#555555",
                "border_color": "#222222",
                "text_color": "#FFFFFF",
            },
        ]

        for cls_data in classes:
            existing = session.exec(
                select(CreatureClass).where(CreatureClass.name == cls_data["name"])
            ).first()
            if not existing:
                print(f"Seeding class: {cls_data['name']}")
                session.add(CreatureClass(**cls_data))

        session.commit()

        # Seed Creatures
        # Using hardcoded image URLs for reproducibility.
        creatures = [
            {
                "name": "Smaug",
                "creature_type": "Dragon",
                "description": "A fire breathing dragon.",
                "image_url": "https://api.dicebear.com/7.x/identicon/svg?seed=Smaug",
            },
            {
                "name": "Dire Wolf",
                "creature_type": "Beast",
                "description": "A large wolf.",
                "image_url": "https://api.dicebear.com/7.x/identicon/svg?seed=DireWolf",
            },
        ]

        for c_data in creatures:
            existing = session.exec(
                select(Creature).where(Creature.name == c_data["name"])
            ).first()
            if not existing:
                print(f"Seeding creature: {c_data['name']}")
                # Initialize timestamps.
                from datetime import datetime, timezone

                db_creature = Creature(**c_data)
                db_creature.last_modify = datetime.now(timezone.utc).isoformat()

                session.add(db_creature)

        session.commit()
        print("Seeding complete.")


if __name__ == "__main__":
    seed_data()
