from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse
from app.schemas.post import PostCreate  # Assuming you have a PostCreate schema defined
from app.models.post import Post  # Assuming you have a Post model defined
from app.database import get_db  # Assuming you have a database session dependency

router = APIRouter()

@router.post("/add")
async def add_post(post: PostCreate, db: Session = Depends(get_db)):
    title = post.title.upper()
    content = post.content.lower()
    db_post = Post(title=title, content=content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "success": True,
            "message": "Post created successfully",
            "data": {
                "id": db_post.id,
                "title": db_post.title,
                "content": db_post.content,
            }
        }
    )
    