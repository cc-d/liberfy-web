# api/crud.py
from sqlalchemy.orm import Session
from models import User
from schemas import UserDB, UserCreate
from auth import get_password_hash


def create_user(db: Session, userdata: UserCreate) -> UserDB:
    db_user = User(
        email=userdata.email, hpass=get_password_hash(userdata.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
