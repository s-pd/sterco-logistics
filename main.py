from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routers import trips, auth

app = FastAPI(title="Sterco Logistics")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trips.router)
app.include_router(auth.router)

# Serve the frontend
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Optional: serve other static files if needed later
# app.mount("/static", StaticFiles(directory=frontend_path), name="static")

print("Sterco Logistics is running!")