from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date as date_lib
from fastapi import Query
from apps import core

app = FastAPI()

# -------------------------
# Health check
# -------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}

# -------------------------
# Request model
# -------------------------

class ActivityCreate(BaseModel):
    title: str
    category: str
    location: str
    time: str
    date: Optional[str] = None

# -------------------------
# Endpoints
# -------------------------

@app.post("/activities", status_code=status.HTTP_201_CREATED)
def create_activity(activity: ActivityCreate):
    """
    Create a new activity.
    If date is not provided, defaults to today.
    """

    # Default date logic (API responsibility)
    activity_date = activity.date or date_lib.today().isoformat()

    try:
        core.create_activity(
            title=activity.title,
            category=activity.category,
            location=activity.location,
            date=activity_date,
            time=activity.time
        )
    except ValueError as exc:
        # Translate domain error → HTTP error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    return {
        "status": "success",
        "message": "Activity created",
        "date_used": activity_date
    }


@app.get("/activities")
def list_activities(category: Optional[str] = Query(default=None)):
    """
    List activities.
    Optionally filter by category.
    """

    if category:
        filtered = core.find_activities_by_category(category)
        activities = [a.summary() for a in filtered]
    else:
        activities = core.list_activities()

    return {
        "count": len(activities),
        "activities": activities
    }

@app.get("/activities/{activity_id}")
def get_activity(activity_id: str):
    activity = core.get_activity_by_id(activity_id)
    if activity:
        return activity.to_dict()

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Activity not found"
    )

@app.delete("/activities/{activity_id}")
def delete_activity(activity_id: str):
    deleted = core.delete_activity(activity_id)

    if deleted:
        return {"status": "success", "message": "Activity deleted"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Activity not found"
    )
