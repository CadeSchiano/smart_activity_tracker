from fastapi import FastAPI, status, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt

from apps.database import engine, Base
from apps import core
from apps import ai

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# ---------------- AUTH ----------------
SECRET_KEY = "secret"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

fake_user = {"username": "admin", "password": "admin"}


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/login")
def login(data: dict):
    if data["username"] == "admin" and data["password"] == "admin":
        token = jwt.encode(
            {"sub": data["username"], "exp": datetime.utcnow() + timedelta(hours=2)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


# ---------------- MODEL ----------------
class ActivityCreate(BaseModel):
    title: str
    category: str
    location: str
    time: str
    date: Optional[str] = None


# ---------------- ROUTES ----------------
@app.get("/activities")
def list_activities(user=Depends(verify_token)):
    activities = [a.to_dict() for a in core.get_all_activities()]
    return {"activities": activities}


@app.post("/activities")
def create_activity(activity: ActivityCreate, user=Depends(verify_token)):
    activity_date = activity.date or datetime.today().isoformat()

    created = core.create_activity(
        activity.title,
        activity.category,
        activity.location,
        activity_date,
        activity.time
    )
    return created.to_dict()


@app.put("/activities/{activity_id}")
def update_activity(activity_id: str, activity: ActivityCreate, user=Depends(verify_token)):
    existing = core.get_activity_by_id(activity_id)

    if not existing:
        raise HTTPException(status_code=404)

    existing.title = activity.title
    existing.category = activity.category
    existing.location = activity.location
    existing.date = activity.date
    existing.time = activity.time

    from apps.database import SessionLocal
    db = SessionLocal()
    db.merge(existing)
    db.commit()
    db.close()

    return existing.to_dict()


@app.delete("/activities/{activity_id}")
def delete_activity(activity_id: str, user=Depends(verify_token)):
    core.delete_activity(activity_id)
    return {"status": "deleted"}


# ---------------- AI ----------------
@app.get("/ai/ask")
def ask_ai(q: str, user=Depends(verify_token)):
    return {"answer": ai.ask_question(q)}


@app.get("/ai/summary")
def summary(user=Depends(verify_token)):
    return {"summary": ai.summarize_activities()}