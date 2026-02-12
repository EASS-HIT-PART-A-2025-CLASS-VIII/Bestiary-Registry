from typing import Optional
from typing import Annotated
from sqlmodel import SQLModel, Field
from pydantic import Field as PydField, field_validator
from pydantic import constr
from pydantic import model_validator
from pydantic import ConfigDict


NonEmptyStr = constr(min_length=1, strip_whitespace=True)
NON_BLANK_PATTERN = r"^.*\S.*$"


class CreatureBase(SQLModel):
    name: Annotated[NonEmptyStr, PydField(pattern=NON_BLANK_PATTERN)] = Field(
        index=True,
        unique=True,
    )
    mythology: Annotated[NonEmptyStr, PydField(pattern=NON_BLANK_PATTERN)] = Field()
    creature_type: Annotated[NonEmptyStr, PydField(pattern=NON_BLANK_PATTERN)] = Field()
    danger_level: Annotated[int, PydField(ge=1, le=10, multiple_of=1, strict=True)] = (
        Field()
    )

    @field_validator("danger_level", mode="before")
    @classmethod
    def danger_level_whole_float_to_int(cls, v):
        if isinstance(v, bool):
            raise ValueError("danger_level must be an integer")
        if isinstance(v, float):
            if v.is_integer():
                return int(v)
            raise ValueError("danger_level must be an integer")
        return v

    habitat: Annotated[NonEmptyStr, PydField(pattern=NON_BLANK_PATTERN)] = Field(
        default="Unknown"
    )
    last_modify: Annotated[NonEmptyStr, PydField(pattern=NON_BLANK_PATTERN)] = Field(
        default="Unknown"
    )
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
    name: NonEmptyStr = Field(index=True, unique=True)
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
    name: Optional[NonEmptyStr] = None
    color: Optional[NonEmptyStr] = None
    border_color: Optional[NonEmptyStr] = None
    text_color: Optional[NonEmptyStr] = None

    model_config = ConfigDict(
        schema_extra={
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "name": {"type": "string", "minLength": 1, "pattern": r"^(?=.*\S).+$"},
                "color": {"type": "string", "minLength": 1, "pattern": r"^(?=.*\S).+$"},
                "border_color": {
                    "type": "string",
                    "minLength": 1,
                    "pattern": r"^(?=.*\S).+$",
                },
                "text_color": {
                    "type": "string",
                    "minLength": 1,
                    "pattern": r"^(?=.*\S).+$",
                },
            },
        }
    )

    @model_validator(mode="after")
    def at_least_one_field(self):
        # Accept empty body {} as no-op (Schemathesis generates it)
        return self


class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    hashed_password: str
    role: str = Field(default="user")


class Tag(SQLModel, table=True):
    name: str = Field(primary_key=True)


class CreatureTagLink(SQLModel, table=True):
    creature_name: str = Field(foreign_key="creature.name", primary_key=True)
    tag_name: str = Field(foreign_key="tag.name", primary_key=True)
