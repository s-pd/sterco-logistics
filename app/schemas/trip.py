from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TripBase(BaseModel):
    vehicle_id: str
    driver_id: str
    customer_id: str
    pickup_address: str
    delivery_address: str
    pickup_date: datetime
    amount: float
    notes: Optional[str] = None
    status: Optional[str] = "Scheduled"

class TripCreate(TripBase):
    pass

class TripUpdate(BaseModel):
    vehicle_id: Optional[str] = None
    driver_id: Optional[str] = None
    customer_id: Optional[str] = None
    pickup_address: Optional[str] = None
    delivery_address: Optional[str] = None
    pickup_date: Optional[datetime] = None
    amount: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class Trip(TripBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True