from fastapi import FastAPI
from app.routers import auth

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

app.include_router(auth.router, prefix="/auth", tags=["auth"])

