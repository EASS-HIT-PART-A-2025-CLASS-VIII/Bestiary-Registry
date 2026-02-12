from fastapi import APIRouter, Path, HTTPException, Response, status
from app.db import SessionDep
from app.models import (
    CreatureClass,
    CreatureClassCreate,
    CreatureClassRead,
    CreatureClassUpdate,
)
from app.services import classes as service


MAX_INT32 = 2_147_483_647

router = APIRouter(prefix="/classes", tags=["classes"])


@router.post(
    "/",
    response_model=CreatureClassRead,
    responses={
        400: {"description": "Malformed JSON body"},
        409: {"description": "Class already exists"},
    },
)
def create_class(class_data: CreatureClassCreate, session: SessionDep):
    """Create a new creature class."""
    return service.create_class(session, class_data)


@router.get("/", response_model=list[CreatureClassRead])
def read_classes(session: SessionDep):
    """List all available creature classes."""
    return service.list_classes(session)


@router.delete(
    "/{class_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Deleted"},
        404: {"description": "Class not found"},
    },
)
def delete_class(session: SessionDep, class_id: int = Path(..., ge=1, le=MAX_INT32)):
    obj = session.get(CreatureClass, class_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Class not found")

    session.delete(obj)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{class_id}",
    response_model=CreatureClassRead,
    responses={
        400: {"description": "Malformed JSON body"},
        404: {"description": "Class not found"},
        409: {"description": "Conflict"},
    },
)
def update_class_endpoint(
    session: SessionDep,
    class_update: CreatureClassUpdate,
    class_id: int = Path(..., ge=1, le=MAX_INT32),
) -> CreatureClassRead:
    return service.update_class(session, class_id, class_update)
