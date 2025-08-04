from app.core.database import engine, Base
from app.users.models import User
from app.location.models import Address


Base.metadata.create_all(bind=engine)