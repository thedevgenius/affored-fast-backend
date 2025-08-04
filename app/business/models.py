import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.core.database import Base
from app.core.config import TIMEZONE

class Business(Base):
    __tablename__ = "businesses"

    id = Column(PG_UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
