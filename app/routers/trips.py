from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.trip import Trip, TripCreate, TripUpdate
from app.services import trip_service

router = APIRouter(prefix="/trips", tags=["Trips"])

@router.get("/", response_model=list[Trip])
def get_trips(db: Session = Depends(get_db)):
    return trip_service.get_all_trips(db)

@router.post("/", response_model=Trip)
def create_new_trip(trip: TripCreate, db: Session = Depends(get_db)):
    return trip_service.create_trip(db, trip)

@router.get("/{trip_id}", response_model=Trip)
def get_single_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = trip_service.get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.put("/{trip_id}", response_model=Trip)
def update_existing_trip(trip_id: int, trip: TripUpdate, db: Session = Depends(get_db)):
    updated = trip_service.update_trip(db, trip_id, trip)
    if not updated:
        raise HTTPException(status_code=404, detail="Trip not found")
    return updated

@router.delete("/{trip_id}")
def delete_existing_trip(trip_id: int, db: Session = Depends(get_db)):
    deleted = trip_service.delete_trip(db, trip_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"message": "Trip deleted successfully"}