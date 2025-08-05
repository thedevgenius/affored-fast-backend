import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(5), nullable=False)
    zip_code = Column(String(20), nullable=False)
    lat = Column(String(20), nullable=True)
    lng = Column(String(20), nullable=True)
    geohash = Column(String(20), nullable=True)
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return (
            f"<Address(id={self.id}, user_id={self.user_id}, city='{self.city}', state='{self.state}')>"
        )
