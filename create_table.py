from app.core.database import engine, Base
from app.users.models import User


Base.metadata.create_all(bind=engine)