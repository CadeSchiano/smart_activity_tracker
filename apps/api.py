from fastapi import FastAPI, status, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import date as date_lib

from apps.database import engine, Base
from apps import core
from apps import ai

app = FastAPI(
    title="Smart Activity Tracker API",
    description="A REST API for managing activities with FastAPI and SQLAlchemy",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


class ActivityCreate(BaseModel):
    title: str
    category: str
    location: str
    time: str
    date: Optional[str] = None


@app.get("/")
def root():
    return {
        "message": "Smart Activity Tracker API",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/activities", status_code=status.HTTP_201_CREATED)
def create_activity(activity: ActivityCreate):
    activity_date = activity.date or date_lib.today().isoformat()

    try:
        created_activity = core.create_activity(
            title=activity.title,
            category=activity.category,
            location=activity.location,
            date=activity_date,
            time=activity.time
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )

    return created_activity.to_dict()


@app.get("/activities")
def list_activities(category: Optional[str] = Query(default=None)):

    if category:
        filtered = core.find_activities_by_category(category)
        activities = [a.to_dict() for a in filtered]
    else:
        activities = [a.to_dict() for a in core.get_all_activities()]

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
        return {
            "status": "success",
            "deleted_id": activity_id
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Activity not found"
    )

@app.delete("/activities")
def delete_all_activities():
    activities = core.get_all_activities()
    for a in activities:
        core.delete_activity(a.id)
    return {"status": "all activities deleted"}

@app.get("/ai/summary")
def ai_summary():
    return {
        "summary": ai.summarize_activities()
    }


@app.get("/ai/ask")
def ai_ask(q: str):
    return {
        "question": q,
        "answer": ai.ask_question(q)
    }