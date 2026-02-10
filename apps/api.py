from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date as date_lib

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
def list_activities():
    """
    List all activities as summaries.
    """
    activities = core.list_activities()

    return {
        "count": len(activities),
        "activities": activities
    }
