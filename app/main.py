from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routes import auth, habits

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API")

# ✅ FIX: ADD CORS MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)
app.include_router(habits.router)

@app.get("/")
def root():
    return {"status": "Backend running successfully"}