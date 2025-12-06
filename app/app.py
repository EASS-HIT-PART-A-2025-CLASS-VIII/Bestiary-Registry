from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory "database"
items_db = {}
# Simple in-memory ID counter
counter_id = 1


# Pydantic models
class CreatureCreate(BaseModel):
    name: str
    mythology: str
    creature_type: str
    danger_level: int


class CreatureRead(BaseModel):
    id: int
    name: str
    mythology: str
    creature_type: str
    danger_level: int


# API Endpoints
@app.post("/creatures/")
def create_creature(creature: CreatureCreate) -> CreatureRead:
    global counter_id
    creature_id = counter_id
    counter_id += 1
    creature_dict = {
        "id": creature_id,
        "name": creature.name,
        "mythology": creature.mythology,
        "creature_type": creature.creature_type,
        "danger_level": creature.danger_level,
    }
    items_db[creature_id] = creature_dict

    return CreatureRead(**creature_dict)


@app.get("/creatures/")
def get_creatures() -> list[CreatureRead]:
    creatures = []
    for creature_dict in items_db.values():
        creatures.append(CreatureRead(**creature_dict))
    return creatures


@app.put("/creatures/{creature_id}")
def update_creature(creature_id: int, creature: CreatureCreate) -> CreatureRead:
    if creature_id not in items_db:
        raise HTTPException(status_code=404, detail="Creature not found")

    creature_dict = {
        "id": creature_id,
        "name": creature.name,
        "mythology": creature.mythology,
        "creature_type": creature.creature_type,
        "danger_level": creature.danger_level,
    }
    items_db[creature_id] = creature_dict

    return CreatureRead(**creature_dict)


@app.delete("/creatures/{creature_id}")
def delete_creature(creature_id: int) -> dict:
    if creature_id not in items_db:
        raise HTTPException(status_code=404, detail="creature not found")

    del items_db[creature_id]

    return {"detail": "creature deleted successfully"}
