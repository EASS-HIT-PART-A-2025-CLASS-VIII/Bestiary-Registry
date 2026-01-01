from typing import Optional
from sqlmodel import SQLModel, Field


class CreatureBase(SQLModel):
    name: str = Field(index=True)
    mythology: str
    creature_type: str
    danger_level: int
    habitat: str = Field(default="Unknown")
    image_url: str = Field(default="")


class Creature(CreatureBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CreatureCreate(CreatureBase):
    pass


class CreatureRead(CreatureBase):
    id: int
