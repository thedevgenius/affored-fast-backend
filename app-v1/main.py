from fastapi import FastAPI

from app.routers import post
from app.auth import auth

app = FastAPI()

app.include_router(post.router, prefix="/post", tags=["posts"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
