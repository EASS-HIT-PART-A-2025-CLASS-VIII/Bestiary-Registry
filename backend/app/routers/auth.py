from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

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


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    # Authenticate user credentials.
    user = session.get(User, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
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


@router.post("/register")
def register(username: str, password: str, session: SessionDep, role: str = "user"):
    existing = session.get(User, username)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = get_password_hash(password)
    user = User(username=username, hashed_password=hashed, role=role)
    session.add(user)
    session.commit()
    return {"username": username, "status": "created"}


@router.post("/admin/rotate-keys")
async def rotate_keys(current_user: Annotated[dict, Depends(get_admin_user)]):
    return {"status": "keys rotated", "user": current_user["username"]}
