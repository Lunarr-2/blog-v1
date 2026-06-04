from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
import uuid
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., example="tolu1")
    email: EmailStr = Field(..., example="tolu@example.com")

class UserCreate(UserBase):
    password : str = Field(..., min_length=8, example="password123")

class UserPublic(BaseModel):
    id: uuid.UUID
    username: str

    model_config = ConfigDict(from_attributes=True)

class UserPrivate(UserPublic):
    id: uuid.UUID
    username: str

class PostCreate(BaseModel):
    title : str = Field(...,example="This is Title 1")
    content: str = Field(..., example="This is a content Example")
    url : str 
    file_type: str
    file_name: str
    created_at: datetime
    

class PostResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    url: str
    file_type: str
    file_name: str
    

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token : str
    token_type: str = "bearer"
