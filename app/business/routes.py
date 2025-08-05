from fastapi import APIRouter, HTTPException, status, Response, Depends, Request
from sqlalchemy.orm import Session
from app.business.models import Business
from app.core.database import get_db
from fastapi.responses import JSONResponse
from .schemas import BusinessCreate

router = APIRouter()

@router.post('/business/add', name='Add Business')
async def add_business(data: BusinessCreate, db: Session = Depends(get_db)):
    """Add a new business."""
    business = Business(
        name=data.name,
        description=data.description
    )
    db.add(business)
    db.commit()
    db.refresh(business)
    if not business:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create business"
        )
    # Return the created business
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "success": True,
            "message": "Business added successfully",
            "data": business
        }
    )