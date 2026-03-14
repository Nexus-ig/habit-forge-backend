from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app import models
from app.database import SessionLocal
from app.schemas import HabitCreate
from app.deps import get_current_user, paid_user_only

router = APIRouter(prefix="/habits")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Only PAID users can create habits
@router.post("")
def create_habit(
    habit: HabitCreate,
    user=Depends(paid_user_only),
    db: Session = Depends(get_db)
):
    new_habit = models.Habit(
        user_id=user.id,
        title=habit.title,
        category=habit.category,
        priority_level=habit.priority_level,
        frequency=habit.frequency
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit

# Everyone logged in can view their habits
@router.get("")
def get_habits(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Habit).filter(models.Habit.user_id == user.id).all()

# Everyone logged in can log habits
@router.post("/{habit_id}/log")
def log_habit(habit_id: str, status: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    log = models.HabitLog(
        habit_id=habit_id,
        date=date.today(),
        status=status
    )
    db.add(log)
    db.commit()
    return {"message": "Logged"}
