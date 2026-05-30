from fastapi import FastAPI
from schema import PostCreate,  PostResponse
from contextlib import asynccontextmanager
from database import get_db, Base, engine
from routers import posts
import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(posts.router, prefix="/api/posts", tags=["posts"])

# posts_db = []

@app.get("/")
def check_health():
    return {"status" : "healthy"}


