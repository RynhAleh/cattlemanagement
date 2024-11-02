from pydantic import BaseModel
from datetime import date
from sqlalchemy import Column, Integer, Float, String, Date
from database import Base
from typing import Optional


class Cattle(Base):
    __tablename__ = "cattle"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    color = Column(String)
    breed = Column(String)
    birthdate = Column(Date)


class CattleSchema(BaseModel):
    id: Optional[int] = 0
    name: str
    color: str
    breed: str
    birthdate: date

    class Config:
        orm_mode = True


class Milking(Base):
    __tablename__ = "milking"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    fio = Column(String)
    cows = Column(Integer)
    milk = Column(Float)
    milk_e = Column(Float)
    milk_h = Column(Float)
    milk_1 = Column(Float)
    fat = Column(Float)
    prot = Column(Float)


class MilkingSchema(BaseModel):
    id: Optional[int] = 0
    date: date
    fio: str
    cows: int
    milk: float
    milk_e: float
    milk_h: float
    milk_1: float
    fat: float
    prot: float

    class Config:
        orm_mode = True


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class UserSchema(BaseModel):
    username: str
    password: str
