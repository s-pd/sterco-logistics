from sqlalchemy import text
from sqlalchemy.orm import Session
from app.schemas.trip import TripCreate, TripUpdate
from typing import List, Optional

def get_all_trips(db: Session):
    result = db.execute(text("SELECT * FROM trips ORDER BY id DESC"))
    return [dict(row._mapping) for row in result]

def get_trip_by_id(db: Session, trip_id: int):
    result = db.execute(text("SELECT * FROM trips WHERE id = :id"), {"id": trip_id})
    row = result.fetchone()
    return dict(row._mapping) if row else None

def create_trip(db: Session, trip: TripCreate):
    query = text("""
        INSERT INTO trips (vehicle_id, driver_id, customer_id, pickup_address, 
                          delivery_address, pickup_date, amount, notes, status)
        VALUES (:vehicle_id, :driver_id, :customer_id, :pickup_address, 
                :delivery_address, :pickup_date, :amount, :notes, :status)
        RETURNING *
    """)
    result = db.execute(query, trip.model_dump())
    db.commit()
    return dict(result.fetchone()._mapping)

def update_trip(db: Session, trip_id: int, trip: TripUpdate):
    # Only update fields that were actually sent
    update_data = {k: v for k, v in trip.model_dump().items() if v is not None}
    
    if not update_data:
        return get_trip_by_id(db, trip_id)

    set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
    update_data["id"] = trip_id

    query = text(f"""
        UPDATE trips 
        SET {set_clause}
        WHERE id = :id
        RETURNING *
    """)
    
    result = db.execute(query, update_data)
    db.commit()
    row = result.fetchone()
    return dict(row._mapping) if row else None

def delete_trip(db: Session, trip_id: int):
    result = db.execute(text("DELETE FROM trips WHERE id = :id RETURNING id"), {"id": trip_id})
    db.commit()
    return result.fetchone() is not None