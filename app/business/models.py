import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.core.database import Base
from app.core.config import TIMEZONE

class Business(Base):
    __tablename__ = "businesses"

    id = Column(PG_UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    phone = Column(String(20), nullable=True)
    phone_alt = Column(String(20), nullable=True)
    whatsapp = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    
    address_id = Column(PG_UUID(as_uuid=True), ForeignKey('addresses.id'), nullable=False, index=True)
    geohash = Column(String(20), nullable=True)

    logo = Column(String, nullable=True)
    cover_image = Column(String, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)