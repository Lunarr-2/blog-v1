from fastapi import APIRouter,status,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from schema import UserPublic, UserCreate, Token
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from models import User

from utils.auth import create_access_token, verify_access_token, hash_password, verify_password, CURRENT_USER
from datetime import timedelta, UTC, datetime
from config import settings
import uuid






router = APIRouter()


@router.get("", response_model=list[UserPublic], status_code=status.HTTP_200_OK, summary="List of all users")
async def get_all_user(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User).order_by(User.id.desc()))
    users = result.scalars().all()

    return users


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED, summary="Creating a new user")
async def create_user(user: UserCreate,
                      db: Annotated[AsyncSession, Depends(get_db)]):
    

    try: 
        result = await db.execute(select(User).where(func.lower(User.email)  == user.email.lower()))
        exisiting_user = result.scalars().first()

        if exisiting_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This Email address is already in use"
            )
        else :
    
            new_user = User(
                username = user.username,
                email =  user.email,
                password_hash = hash_password(user.password)
            )

            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

            return new_user
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

@router.post("/token", response_model=Token, summary="Login for users")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     db: Annotated[AsyncSession, Depends(get_db)]):
    
    try:

        result = await db.execute(select(User).where(func.lower(User.email) == form_data.username.lower()))

        user = result.scalars().first()


        if not user or not verify_password(form_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="email or password do not match",
                headers={"WWW-Authenticate" : "Bearer"}
            )
        

        access_token_expire = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data = {"sub" : str(user.id)},
            expires_delta= access_token_expire
        )


        return Token(access_token=access_token, token_type="bearer")
    
    except Exception as e :
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= str(e)
        )
