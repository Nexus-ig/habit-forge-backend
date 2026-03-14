from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

# JWT Config
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

# Bearer auth (Swagger will show "Authorize" with token box)
security = HTTPBearer()

# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get logged-in user from JWT
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# Paid-user guard (for premium features)
def paid_user_only(user=Depends(get_current_user)):
    if not user.is_paid_user:
        raise HTTPException(
            status_code=403,
            detail="Upgrade required to use this feature"
        )
    return user
