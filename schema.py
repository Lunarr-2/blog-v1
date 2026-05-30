from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
import uuid
from datetime import datetime

class PostCreate(BaseModel):
    title : str = Field(...,example="This is Title 1")
    content: str = Field(..., example="This is a content Example")
    url : str 
    file_type: str
    file_name: str
    

class PostResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    url: str
    file_type: str
    file_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


