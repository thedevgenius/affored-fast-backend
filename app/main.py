from fastapi import FastAPI

from app.routes import post



app = FastAPI()
app.include_router(post.router, prefix="/post", tags=["posts"])
