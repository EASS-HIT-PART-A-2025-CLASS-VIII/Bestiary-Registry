from typing import Optional
from sqlmodel import SQLModel, Field


class CreatureBase(SQLModel):
    name: str = Field(index=True, unique=True)
    mythology: str
    creature_type: str
    danger_level: int
    habitat: str = Field(default="Unknown")
    last_modify: str = Field(default="Unknown")
    image_url: Optional[str] = Field(default=None)
    image_status: str = Field(default="pending")  # Status: pending, ready, failed
    image_error: Optional[str] = Field(default=None)


class Creature(CreatureBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CreatureCreate(CreatureBase):
    pass


class CreatureRead(CreatureBase):
    id: int


class CreatureClassBase(SQLModel):
    name: str = Field(index=True, unique=True)
    color: str = Field(default="rgba(127,19,236,0.1)")  # CSS background color
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


class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    hashed_password: str
    role: str = Field(default="user")


class Tag(SQLModel, table=True):
    name: str = Field(primary_key=True)


class CreatureTagLink(SQLModel, table=True):
    creature_name: str = Field(foreign_key="creature.name", primary_key=True)
    tag_name: str = Field(foreign_key="tag.name", primary_key=True)
