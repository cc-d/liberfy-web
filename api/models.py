# api/models.py
from sqlalchemy import Column, Integer, String
from db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hpassword = Column(String)
