from pydantic import BaseModel, Field
from typing import Optional


class PostCreate(BaseModel):
    title : str = Field(...,example="This is Title 1")
    content: str = Field(..., example="This is a content Example")
    url : str 
    file_type: str
    file_name: str
    

class PostResponse(BaseModel):
    title : str
    content: str


