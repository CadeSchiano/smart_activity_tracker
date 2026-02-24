import uuid
from sqlalchemy import Column, String
from apps.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    location = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "location": self.location,
            "date": self.date,
            "time": self.time
        }
