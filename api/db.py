from config import DATABASE_URL
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, class_mapper, DeclarativeMeta, Session

Base = declarative_base()
AsyncSessionLocal = sessionmaker(
    bind=create_async_engine(DATABASE_URL, echo=True),
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()


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


async def async_add_com_ref(
    model: DeclarativeMeta, db=Depends(get_db)
) -> DeclarativeMeta:
    """Add a model instance to the database and return the instance with
    the database-generated id
    """
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model
