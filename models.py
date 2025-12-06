from typing import Optional
from sqlmodel import SQLModel, Field


# SQLModel model for Creature
class Creature(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    mythology: int
    creature_type: str
    danger_level: int
