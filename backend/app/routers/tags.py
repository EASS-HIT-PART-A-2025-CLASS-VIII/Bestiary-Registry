from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import select
from app.db import SessionDep
from app.models import Tag, CreatureTagLink, Creature

router = APIRouter(tags=["tags"])


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1)


@router.get("/tags", response_model=list[Tag])
def list_tags(session: SessionDep):
    return session.exec(select(Tag)).all()


@router.post(
    "/tags",
    response_model=Tag,
    responses={
        400: {"description": "Invalid JSON body"},
        409: {"description": "Tag already exists"},
    },
)
def create_tag(tag: TagCreate, session: SessionDep):
    name = tag.name.strip()

    existing = session.get(Tag, name)
    if existing:
        raise HTTPException(status_code=409, detail="Tag already exists")

    new_tag = Tag(name=name)
    session.add(new_tag)
    session.commit()
    session.refresh(new_tag)
    return new_tag


@router.post(
    "/creatures/{creature_name}/tags/{tag_name}",
    responses={
        404: {"description": "Creature or Tag not found"},
        409: {"description": "Already tagged"},
    },
)
def add_tag_to_creature(creature_name: str, tag_name: str, session: SessionDep):
    creature = session.exec(
        select(Creature).where(Creature.name == creature_name)
    ).first()
    if not creature:
        raise HTTPException(status_code=404, detail="Creature not found")

    tag = session.get(Tag, tag_name)
    if not tag:
        # Tag must exist to be linked.
        raise HTTPException(status_code=404, detail="Tag not found")

    link = CreatureTagLink(creature_name=creature_name, tag_name=tag_name)
    session.add(link)
    try:
        session.commit()
    except Exception:
        session.rollback()  # Handle duplicate entry.
        raise HTTPException(status_code=409, detail="Already tagged")

    return {"status": "tagged"}
