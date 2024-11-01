from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List
from sqlalchemy.orm import Session
from models import Cattle, CattleSchema, User, UserSchema
from auth import create_access_token, create_user, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from database import SessionLocal
from datetime import timedelta

router = APIRouter()


def get_session_local():
    yield SessionLocal()


@router.get("/api/cattle", response_model=List[CattleSchema])
async def read_cattle(
    limit: int = Query(None, ge=1),  # Минимум 1 запись
    offset: int = Query(0, ge=0),  # Смещение не меньше 0
    db: Session = Depends(get_session_local)
):
    cattle_records = db.query(Cattle).offset(offset).limit(limit).all()
    return cattle_records if cattle_records else []


@router.post("/api/cattle", response_model=CattleSchema)
def create_cattle(cattle: CattleSchema, db: Session = Depends(get_session_local)):
    # Создаем запись о животном на основе переданных данных
    db_cattle = Cattle(name=cattle.name, color=cattle.color, breed=cattle.breed, birthdate=cattle.birthdate)
    db.add(db_cattle)
    db.commit()  # Сохраняем изменения в базе данных
    db.refresh(db_cattle)  # Обновляем объект, чтобы получить его id
    return db_cattle


@router.post("/api/register", response_model=UserSchema)
async def register(user: UserSchema, db: Session = Depends(get_session_local)):
    existing_user = db.query(User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)


@router.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session_local)):
    user = db.query(User).filter_by(username=form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
