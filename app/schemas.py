from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    is_paid_user: bool

class HabitCreate(BaseModel):
    title: str
    category: str | None = None
    priority_level: str | None = None
    frequency: str | None = None
