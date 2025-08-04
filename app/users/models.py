import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.core.database import Base
from .utils import generate_random_color
from app.core.config import TIMEZONE

class User(Base):
    __tablename__ = 'users'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('Asia/Kolkata', now())"))
    profile_color = Column(String, nullable=True, default=generate_random_color())
    geohash = Column(String, nullable=True)