from fastapi import HTTPException,status,Depends
import jwt 
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from datetime import datetime, timedelta, UTC
from config import settings
import uuid
from typing import  Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func,select
from models import User



password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")


def hash_password(plain_password: str):
    return password_hasher.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str):
    return password_hasher.verify(plain_password,hashed_password)


def create_access_token(data: dict, expires_delta: timedelta| None):

    to_encode = data.copy()


    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else :
        expire = datetime.now(UTC) + timedelta(settings.access_token_expire_minutes)


    to_encode.update({"exp" : expire})


    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )

    return encoded_jwt


def verify_access_token (token : str) -> uuid :
    try:
        to_decode = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require" : ["sub", "exp"]}
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This token is invalid"
        )
    else :
        
        return to_decode.get("sub")
        

async def get_current_user( token : Annotated[str, Depends(oauth2_scheme)],
                           db : Annotated[AsyncSession, Depends(get_db)]):
    
    user_id = verify_access_token(token)

    if user_id is None :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    

    try :
        
        user_id_uuid = uuid.UUID(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid User Id in Token",
            headers={"WWW-Authenticate" : "Bearer"}
        )

    result = await db.execute(select(User).where(User.id == user_id_uuid))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    return user 


CURRENT_USER = Annotated[User, Depends(get_current_user)]




    
