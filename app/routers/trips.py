from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import text
from ..database import engine
from ..routers.auth import get_current_user   # We'll create this next

router = APIRouter(prefix="/trips", tags=["Trips"])

class TripCreate(BaseModel):
    vehicle_id: str
    driver_id: str
    customer_id: str
    pickup_address: str
    delivery_address: str
    pickup_date: datetime
    amount: float
    notes: Optional[str] = None

class TripUpdate(BaseModel):
    pickup_address: Optional[str] = None
    delivery_address: Optional[str] = None
    pickup_date: Optional[datetime] = None
    amount: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[str] = None


# ==================== PROTECTED ROUTES ====================

@router.get("/")
async def get_all_trips():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM trips ORDER BY created_at DESC"))
        trips = [dict(row) for row in result.mappings()]
    return {"trips": trips}


@router.post("/")
async def create_trip(trip: TripCreate):
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO trips 
                (vehicle_id, driver_id, customer_id, pickup_address, delivery_address, pickup_date, amount, notes)
                VALUES 
                (:vehicle_id, :driver_id, :customer_id, :pickup_address, :delivery_address, :pickup_date, :amount, :notes)
            """), trip.dict())
            conn.commit()
        return {"message": "Trip created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{trip_id}")
async def update_trip(trip_id: str, trip: TripUpdate, current_user: dict = Depends(get_current_user)):
    try:
        with engine.connect() as conn:
            existing = conn.execute(text("SELECT id FROM trips WHERE id = :id"), {"id": trip_id}).fetchone()
            if not existing:
                raise HTTPException(status_code=404, detail="Trip not found")

            update_data = {k: v for k, v in trip.dict().items() if v is not None}
            if not update_data:
                raise HTTPException(status_code=400, detail="No fields to update")

            set_clause = ", ".join([f"{k} = :{k}" for k in update_data.keys()])
            update_data["id"] = trip_id

            conn.execute(text(f"""
                UPDATE trips 
                SET {set_clause}
                WHERE id = :id
            """), update_data)
            conn.commit()

        return {"message": "Trip updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{trip_id}")
async def delete_trip(trip_id: str, current_user: dict = Depends(get_current_user)):
    try:
        with engine.connect() as conn:
            result = conn.execute(text("DELETE FROM trips WHERE id = :id"), {"id": trip_id})
            conn.commit()
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Trip not found")
        return {"message": "Trip deleted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))