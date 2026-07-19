from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base
import uuid
from datetime import datetime

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registration_number = Column(String, unique=True, nullable=False)
    model = Column(String)
    year = Column(Integer)
    status = Column(String, default="active")
    capacity = Column(Numeric(10,2))
    created_at = Column(DateTime, default=datetime.utcnow)