from apps.database import SessionLocal
from apps.models import Activity


# ---------------- CREATE ----------------
def create_activity(title, category, location, date, time, user_id):
    db = SessionLocal()

    activity = Activity(
        title=title,
        category=category,
        location=location,
        date=date,
        time=time,
        user_id=user_id
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)
    db.close()

    return activity


# ---------------- GET USER ACTIVITIES ----------------
def get_user_activities(user_id):
    db = SessionLocal()

    activities = db.query(Activity).filter(Activity.user_id == user_id).all()

    db.close()
    return activities


# ---------------- DELETE ----------------
def delete_activity(activity_id):
    db = SessionLocal()

    activity = db.query(Activity).filter(Activity.id == activity_id).first()

    if activity:
        db.delete(activity)
        db.commit()

    db.close()
    return True