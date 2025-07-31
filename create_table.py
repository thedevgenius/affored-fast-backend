from app.database import engine, Base
from app.models.post import Post


Base.metadata.create_all(bind=engine)