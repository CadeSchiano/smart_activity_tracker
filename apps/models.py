from sqlalchemy import Column, String
from apps.database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Activity(Base):
    __tablename__ = "activities"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    category = Column(String)
    location = Column(String)
    date = Column(String)
    time = Column(String)
    user_id = Column(String)