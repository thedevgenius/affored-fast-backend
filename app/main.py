from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.business.routes import router as business_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(business_router, prefix="/business", tags=["business"])


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}