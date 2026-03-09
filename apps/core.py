"""
core.py

Core business logic using SQLAlchemy database.
"""

from sqlalchemy.orm import Session
from .database import SessionLocal
from .activity import Activity


def create_activity(title: str, category: str, location: str, date: str, time: str):
    db: Session = SessionLocal()
    try:
        activity = Activity(
            title=title,
            category=category,
            location=location,
            date=date,
            time=time
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity
    finally:
        db.close()


def get_all_activities():
    db: Session = SessionLocal()
    try:
        return db.query(Activity).all()
    finally:
        db.close()


def get_activity_by_id(activity_id: str):
    db: Session = SessionLocal()
    try:
        return db.query(Activity).filter(Activity.id == activity_id).first()
    finally:
        db.close()


def find_activities_by_category(category: str):
    db: Session = SessionLocal()
    try:
        return db.query(Activity).filter(Activity.category == category).all()
    finally:
        db.close()


def delete_activity(activity_id: str) -> bool:
    db: Session = SessionLocal()
    try:
        activity = db.query(Activity).filter(Activity.id == activity_id).first()

        if not activity:
            return False

        db.delete(activity)
        db.commit()
        return True
    finally:
        db.close()
