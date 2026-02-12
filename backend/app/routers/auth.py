from datetime import timedelta
from typing import Annotated, Literal
from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlmodel import select
from pydantic import BaseModel, Field


from app.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_admin_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.db import SessionDep
from app.models import User

router = APIRouter(tags=["auth"])


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    role: Literal["user", "admin"] = "user"


@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect username or password",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect username or password"}
                }
            },
        }
    },
)
async def login_for_access_token(
    session: SessionDep,
    username: str = Form(..., min_length=1),
    password: str = Form(..., min_length=1),
):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/register",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid JSON body"},
        status.HTTP_409_CONFLICT: {"description": "User already exists"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation error"},
    },
)
def register(payload: RegisterRequest, session: SessionDep):
    username = payload.username
    password = payload.password
    role = payload.role

    existing = session.exec(select(User).where(User.username == username)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    hashed = get_password_hash(password)
    user = User(username=username, hashed_password=hashed, role=role)
    session.add(user)
    session.commit()
    return {"username": username, "status": "created"}


@router.post(
    "/admin/rotate-keys",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"},
        status.HTTP_403_FORBIDDEN: {"description": "Not authorized"},
    },
)
async def rotate_keys(current_user: Annotated[dict, Depends(get_admin_user)]):
    return {"status": "keys rotated", "user": current_user["username"]}
