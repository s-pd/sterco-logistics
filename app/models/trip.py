from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base
import uuid
from datetime import datetime

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True))
    driver_id = Column(UUID(as_uuid=True))
    customer_id = Column(UUID(as_uuid=True))
    pickup_address = Column(Text)
    delivery_address = Column(Text)
    pickup_date = Column(DateTime)
    delivery_date = Column(DateTime)
    status = Column(String, default="pending")
    amount = Column(Numeric(12,2))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)