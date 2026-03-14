from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import auth, habits

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API")

app.include_router(auth.router)
app.include_router(habits.router)

@app.get("/")
def root():
    return {"status": "Backend running successfully"}
