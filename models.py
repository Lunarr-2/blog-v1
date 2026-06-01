from sqlalchemy.orm import mapped_column,Mapped, relationship
from sqlalchemy import  String, UUID, DateTime, ForeignKey
from datetime import datetime, UTC
import uuid
from database import Base

from __future__ import annotations


class User(Base):
    __tablename__ = "users"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True, nullable=False, default=uuid.uuid4, index=True)
    username : Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] =mapped_column(String, nullable=False)

    posts : Mapped[list[Post]] = relationship(back_populates="user", cascade= "all, delete-orphan")


class Post(Base):
    __tablename__ = "posts"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True, nullable=False, default=uuid.uuid4)
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    file_type: Mapped[str] = mapped_column(String, nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(UTC), nullable=False)

    user : Mapped[User] = relationship(back_populates="posts")