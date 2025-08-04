from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.core.database import get_db
from app.users.models import User

async def create_user(phone: str, db: Session):
    """Create a new user in the database."""
    db_user = db.query(User).filter_by(phone=phone).first()
    if not db_user:
        db_user = User(phone=phone)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user