from fastapi import FastAPI
from pydantic import BaseModel
from apps import core




app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}



class ActivityCreate(BaseModel):
    title: str
    category: str
    location: str
    time: str

@app.post("/activities")
def create_activity(activity: ActivityCreate):
    core.create_activity(
        title=activity.title,
        category=activity.category,
        location=activity.location,
        time=activity.time
    )
    return {"message": "Activity created"}

@app.get("/activities")
def list_activities():
    return {"activities": core.list_activities()}
