from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
import app.models.user
import app.models.vehicle
import app.models.customer
import app.models.trip

from app.routers.auth import router as auth_router
from app.routers.trips import router as trips_router

app = FastAPI(title="Sterco Logistics")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(trips_router)

@app.get("/")
async def root():
    return {"message": "Sterco Logistics API is running!"}

print("✅ Sterco Logistics Backend Started!")