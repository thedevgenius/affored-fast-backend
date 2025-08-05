from app.core.database import engine, Base
from app.users.models import User
from app.location.models import Address
from app.business.models import Business


Base.metadata.create_all(bind=engine)