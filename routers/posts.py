from fastapi import APIRouter,Depends, HTTPException, status

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from database import get_db
from schema import PostCreate, PostResponse
import models
import uuid


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
async def create_post(post: PostCreate,
                      db:Annotated[AsyncSession, Depends(get_db)]):
    

    new_post = models.Post(
        title = post.title,
        content=post.content,
        url = post.url,
        file_type = post.file_type,
        file_name = post.file_name

    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


@router.delete("/{post_id}")
async def delete_post(post_id: str,
                      db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await db.execute(select(models.Post).where(models.Post.id == post_uuid))

        post = result.scalars().first()

        await db.delete(post)
        await db.commit()

        return {"status" : "Post deleted Successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )