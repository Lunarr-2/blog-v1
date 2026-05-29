from sqlalchemy.orm import DeclarativeBase, mapped_column,Mapped
from sqlalchemy import Text, String, Column, UUID, DateTime, ForeignKey
from datetime import datetime, UTC, timedelta
import uuid


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"
    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True, nullable=False, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    caption: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    file_type: Mapped[str] = mapped_column(String, nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(UTC), nullable=False)