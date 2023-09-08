# api/db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    sessionmaker,
    class_mapper,
    DeclarativeMeta,
    Session,
    DeclarativeBase,
)

from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def model_to_dict(
    model_instance: DeclarativeMeta, exclude_internal: bool = True
) -> dict:
    """Convert SQLAlchemy model to dictionary which should be a subset of
    models defined in the schemas
    """
    if not isinstance(model_instance.__class__, DeclarativeMeta):
        raise ValueError("Input is not a SQLAlchemy model instance.")

    if exclude_internal:
        column_names = [col.name for col in model_instance.__table__.columns]
        data = {
            col_name: getattr(model_instance, col_name)
            for col_name in column_names
        }
    else:
        data = model_instance.__dict__.copy()

    internal_attributes = ["_sa_instance_state"]
    for attr in internal_attributes:
        data.pop(attr, None)

    return data


def add_commit_refresh(obj, db) -> DeclarativeBase:
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
