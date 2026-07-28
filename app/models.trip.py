from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, func
from app.database import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String(50), nullable=False)
    driver_id = Column(String(50), nullable=False)
    customer_id = Column(String(50), nullable=False)
    pickup_address = Column(Text, nullable=False)
    delivery_address = Column(Text, nullable=False)
    pickup_date = Column(DateTime, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String(30), default="Scheduled")
    created_at = Column(DateTime, server_default=func.now())