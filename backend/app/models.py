from typing import Optional
from sqlmodel import SQLModel, Field


class CreatureBase(SQLModel):
    name: str = Field(index=True)
    mythology: str
    creature_type: str
    danger_level: int
    habitat: str = Field(default="Unknown")
    last_modify: str = Field(default="Unknown")
    image_url: str = Field(default="")


class Creature(CreatureBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CreatureCreate(CreatureBase):
    pass


class CreatureRead(CreatureBase):
    id: int


class CreatureClassBase(SQLModel):
    name: str = Field(index=True, unique=True)
    color: str = Field(
        default="rgba(127,19,236,0.1)"
    )  # CSS background value (rgba/hex)
    border_color: str = Field(default="rgba(127,19,236,0.2)")
    text_color: str = Field(default="#ad92c9")


class CreatureClass(CreatureClassBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CreatureClassCreate(CreatureClassBase):
    pass


class CreatureClassRead(CreatureClassBase):
    id: int


class CreatureClassUpdate(SQLModel):
    name: Optional[str] = None
    color: Optional[str] = None
    border_color: Optional[str] = None
    text_color: Optional[str] = None
