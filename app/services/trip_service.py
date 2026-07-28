from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.trip import TripCreate, TripUpdate

def get_all_trips(db: Session):
    query = text("SELECT * FROM trips ORDER BY id DESC")
    result = db.execute(query)
    return [dict(row._mapping) for row in result]

def get_trip_by_id(db: Session, trip_id: int):
    query = text("SELECT * FROM trips WHERE id = :id")
    result = db.execute(query, {"id": trip_id}).fetchone()
    if result:
        return dict(result._mapping)
    return None

def create_trip(db: Session, trip: TripCreate):
    query = text("""
        INSERT INTO trips (vehicle_id, driver_id, customer_id, pickup_address, 
                          delivery_address, pickup_date, amount, notes, status)
        VALUES (:vehicle_id, :driver_id, :customer_id, :pickup_address, 
                :delivery_address, :pickup_date, :amount, :notes, :status)
        RETURNING *
    """)
    result = db.execute(query, trip.dict())
    db.commit()
    return dict(result.fetchone()._mapping)

def update_trip(db: Session, trip_id: int, trip: TripUpdate):
    # Only update fields that were sent
    update_data = {k: v for k, v in trip.dict(exclude_unset=True).items()}
    
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
    if row:
        return dict(row._mapping)
    return None

def delete_trip(db: Session, trip_id: int):
    query = text("DELETE FROM trips WHERE id = :id RETURNING id")
    result = db.execute(query, {"id": trip_id})
    db.commit()
    return result.fetchone() is not None