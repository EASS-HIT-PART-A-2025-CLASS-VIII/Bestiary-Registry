from sqlmodel import Session, select
from app.db import engine
from app.models import Creature


def check_types():
    with Session(engine) as session:
        statement = select(Creature.creature_type).distinct()
        results = session.exec(statement).all()
        print("Existing Types:", results)


if __name__ == "__main__":
    check_types()
