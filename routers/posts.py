from fastapi import APIRouter,Depends, HTTPException, status, File, UploadFile, Form

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from database import get_db
from schema import PostCreate, PostResponse
import models
import uuid
from utils.images import imagekit
import os
import shutil
import tempfile
from utils.auth import CURRENT_USER


router = APIRouter()

@router.get("", response_model=list[PostResponse])
async def get_all_post(db: Annotated[AsyncSession, Depends(get_db)]):

    result = await db.execute(select(models.Post).order_by(models.Post.id))
    posts = result.scalars().all()

    return posts


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: str, 
                   db: Annotated[AsyncSession, Depends(get_db)]):
    
    post_id_uuid = uuid.UUID(post_id)

    result = await db.execute(select(models.Post).where(models.Post.id  == post_id_uuid))
    post = result.scalars().first()
    
    return post


@router.post("", response_model=PostResponse,summary="creating a post")
async def create_post(
                    db: Annotated[AsyncSession, Depends(get_db)],
                    current_user : CURRENT_USER,
                    file: UploadFile = File(...),
                    title: str = Form(...),
                    content: str = Form(...),
                      ):
    

    temp_file_path = None

    try :


        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:

            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
        
        with open(temp_file_path,"rb") as f:
            file_data = f.read()

        upload_result = imagekit.files.upload(
            file = file_data,
            file_name=file.filename,
            use_unique_file_name= True,
            tags= ["backend-uploaded-v1"]

        )

        new_post = models.Post(
            title = title,
            content= content,
            url = upload_result.url,
            file_type =  "video" if file.content_type.startswith("video/") else "image",
            file_name = upload_result.name,
            user_id = current_user.id
            # uuid.UUID("30604a35-860e-43be-8fc0-f5f399448665")

        )

        db.add(new_post)
        await db.commit()
        await db.refresh(new_post)

        return new_post
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    finally :
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        await file.close()


@router.delete("/{post_id}")
async def delete_post(post_id: str,
                      db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await db.execute(select(models.Post).where(models.Post.id == post_uuid))

        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="This Post does not exists")

        await db.delete(post)
        await db.commit()

        return {"status" : "Post deleted Successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )