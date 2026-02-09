import random
from sqlmodel import Session, select
from app.db import engine
from app.models import Creature

NEW_CLASSES = [
    "Draconic",
    "Chimeric",
    "Fae",
    "Titanic",
    "Abyssal",
    "Ethereal",
    "Mythic Beasts",
]


def update_creature_classes():
    with Session(engine) as session:
        statement = select(Creature)
        creatures = session.exec(statement).all()

        count = 0
        for creature in creatures:
            # old_type = creature.creature_type
            new_type = random.choice(NEW_CLASSES)
            creature.creature_type = new_type
            session.add(creature)
            count += 1
            # print(f"Updated {creature.name}: {old_type} -> {new_type}")

        session.commit()
        print(f"Successfully updated {count} creatures to new classes.")


if __name__ == "__main__":
    update_creature_classes()
