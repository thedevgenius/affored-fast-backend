from app.database import engine, Base
from app.models.post import Post
from app.models.user import User


Base.metadata.create_all(bind=engine)