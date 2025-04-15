from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

import models
from database import get_db
from api.auth.utils import (
    hash_password, verify
)
from api.auth.oauth2 import create_access_token
from api.auth.schema import (
    Token, UserLogin, UserCreate
)

router = APIRouter()

@router.post(
    "/create-user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreate
)
async def create_users(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check existing user with async query
    query = select(models.User).filter_by(user_name=user.username)
    result = await db.execute(query)
    check_user = result.scalar_one_or_none()

    if check_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User name {user.username} is existed"
        )

    # Hash password and create new user
    user.password = hash_password(user.password)
    new_user = models.User(
        user_name=user.username,
        password=user.password
    )

    # Add and commit with async syntax
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.post("/login/", response_model=Token)
async def login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    # Check user exists with async query
    query = select(models.User).filter_by(user_name=user_credentials.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password."
        )

    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password."
        )

    auth_key = create_access_token(
        data={"user_id": user.id, "user_name": user.user_name}
    )
    message = "Login successfully."

    return {"message": message, "auth_key": auth_key, "token_type": "bearer"}