from sqlmodel import Session, select
from app.db import engine
from app.models import CreatureClass

DEFAULT_CLASSES = [
    {
        "name": "Draconic",
        "color": "rgba(255, 107, 107, 0.2)",
        "border_color": "rgba(255, 107, 107, 0.8)",
        "text_color": "#ff6b6b",
    },
    {
        "name": "Chimeric",
        "color": "rgba(255, 159, 67, 0.2)",
        "border_color": "rgba(255, 159, 67, 0.8)",
        "text_color": "#ff9f43",
    },
    {
        "name": "Fae",
        "color": "rgba(254, 202, 87, 0.2)",
        "border_color": "rgba(254, 202, 87, 0.8)",
        "text_color": "#feca57",
    },
    {
        "name": "Titanic",
        "color": "rgba(72, 219, 251, 0.2)",
        "border_color": "rgba(72, 219, 251, 0.8)",
        "text_color": "#48dbfb",
    },
    {
        "name": "Abyssal",
        "color": "rgba(84, 160, 255, 0.2)",
        "border_color": "rgba(84, 160, 255, 0.8)",
        "text_color": "#54a0ff",
    },
    {
        "name": "Ethereal",
        "color": "rgba(200, 214, 229, 0.2)",
        "border_color": "rgba(200, 214, 229, 0.8)",
        "text_color": "#c8d6e5",
    },
    {
        "name": "Mythic Beasts",
        "color": "rgba(95, 39, 205, 0.2)",
        "border_color": "rgba(95, 39, 205, 0.8)",
        "text_color": "#5f27cd",
    },
    {
        "name": "Other",
        "color": "rgba(131, 149, 167, 0.2)",
        "border_color": "rgba(131, 149, 167, 0.8)",
        "text_color": "#8395a7",
    },
]


def seed_classes():
    """Seed default creature classes if they do not exist."""
    with Session(engine) as session:
        print("Checking for existing classes...")
        added_count = 0
        for class_data in DEFAULT_CLASSES:
            statement = select(CreatureClass).where(
                CreatureClass.name == class_data["name"]
            )
            results = session.exec(statement).first()

            if not results:
                print(f"Adding new class: {class_data['name']}")
                new_class = CreatureClass(**class_data)
                session.add(new_class)
                added_count += 1
            else:
                print(f"Class already exists: {class_data['name']}")

        session.commit()
        print(f"\nSeeding complete. Added {added_count} new classes.")


if __name__ == "__main__":
    seed_classes()
