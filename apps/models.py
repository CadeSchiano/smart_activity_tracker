from sqlalchemy import Column, String
from apps.database import Base
import uuid


# ---------------- USER ----------------
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


# ---------------- ACTIVITY ----------------
class Activity(Base):
    __tablename__ = "activities"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    category = Column(String)
    location = Column(String)
    date = Column(String)
    time = Column(String)

    # 🔥 LINK TO USER
    user_id = Column(String)