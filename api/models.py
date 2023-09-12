import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hpassword: Mapped[str] = mapped_column(String)

    # One-to-Many relationship with Project
    projects: Mapped[list['Project']] = relationship(
        'Project', back_populates='user'
    )

    syncdirs: Mapped[list['SyncDir']] = relationship(
        'SyncDir', back_populates='user'
    )


class Project(Base):
    __tablename__ = 'projects'
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(
        String, index=True, unique=True, nullable=False, default='New Project'
    )

    user: Mapped[User] = relationship('User', back_populates='projects')

    # One-to-Many relationship with SyncDir
    syncdirs: Mapped[list['SyncDir']] = relationship(
        'SyncDir', back_populates='project'
    )


class SyncDir(Base):
    __tablename__ = 'syncdirs'
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    path: Mapped[str] = mapped_column(String, nullable=False)
    project_id: Mapped[str] = mapped_column(String, ForeignKey('projects.id'))
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'))

    # Many-to-One relationship with Project
    project: Mapped[Project] = relationship(
        'Project', back_populates='syncdirs'
    )

    # One-to-Many relationship with DirFile
    dirfiles: Mapped[list['DirFile']] = relationship(
        'DirFile', back_populates='syncdir'
    )

    user: Mapped[User] = relationship('User', back_populates='syncdirs')


class DirFile(Base):
    __tablename__ = 'dirfiles'
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    relpath: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=True)
    syncdir_id: Mapped[str] = mapped_column(String, ForeignKey('syncdirs.id'))
    checksum: Mapped[str] = mapped_column(String, nullable=True)
    checksum_type: Mapped[str] = mapped_column(
        String, nullable=False, default='md5'
    )

    # Many-to-One relationship with SyncDir
    syncdir: Mapped[SyncDir] = relationship(
        'SyncDir', back_populates='dirfiles'
    )


# i'll use this later probalby
# class Metadata(Base):
#    __tablename__ = 'metadata'
#    dirfile_id: Mapped[str] = mapped_column(
#        String, ForeignKey('dirfiles.id'), primary_key=True
#    )
#    read: Mapped[bool] = mapped_column(Boolean, default=False)
#    write: Mapped[bool] = mapped_column(Boolean, default=False)
#    execute: Mapped[bool] = mapped_column(Boolean, default=False)
