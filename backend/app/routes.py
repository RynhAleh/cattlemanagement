from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List
from sqlalchemy.orm import Session
from models import *
from auth import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from database import SessionLocal
from datetime import timedelta

router = APIRouter()


def get_session_local():
    yield SessionLocal()


@router.post("/api/login")  # , response_model=UserSchema)
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


@router.get("/api/cattle", response_model=List[CattleSchema])
async def read(
    limit: int = Query(None, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_session_local)
):
    records = db.query(Cattle).offset(offset).limit(limit).all()
    return records if records else []


@router.post("/api/cattle", response_model=CattleSchema)
def create(s: CattleSchema, db: Session = Depends(get_session_local)):
    db_obj = Cattle(name=s.name, color=s.color, breed=s.breed, birthdate=s.birthdate)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/api/milking", response_model=List[MilkingSchema])
async def read(
    limit: int = Query(None, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_session_local)
):
    records = db.query(Milking).offset(offset).limit(limit).all()
    return records if records else []


@router.post("/api/milking", response_model=MilkingSchema)
def create(s: MilkingSchema, db: Session = Depends(get_session_local)):
    db_obj = Milking(date=s.date, fio=s.fio, cows=s.cows, milk=s.milk, milk_e=s.milk_e, milk_h=s.milk_h,
                     milk_1=s.milk_1, fat=s.fat, prot=s.prot)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
