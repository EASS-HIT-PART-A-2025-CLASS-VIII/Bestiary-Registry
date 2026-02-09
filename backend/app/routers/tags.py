from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.db import SessionDep
from app.models import Tag, CreatureTagLink, Creature

router = APIRouter(tags=["tags"])


@router.get("/tags", response_model=list[Tag])
def list_tags(session: SessionDep):
    return session.exec(select(Tag)).all()


@router.post("/tags", response_model=Tag)
def create_tag(tag: Tag, session: SessionDep):
    existing = session.get(Tag, tag.name)
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


@router.post("/creatures/{creature_name}/tags/{tag_name}")
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
        return {"status": "already tagged"}

    return {"status": "tagged"}
