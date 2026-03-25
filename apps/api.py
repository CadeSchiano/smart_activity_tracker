from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt

from apps.database import Base, engine, SessionLocal
from apps.models import User
from apps.auth import hash_password, verify_password
from apps import core, ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

SECRET_KEY = "supersecretkey"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# -------- CLEAN RESPONSE --------
def clean(obj):
    data = obj.__dict__.copy()
    data.pop("_sa_instance_state", None)
    return data


# -------- AUTH --------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")

        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        db.close()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid user")

        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/register")
def register(data: dict):
    db = SessionLocal()

    existing = db.query(User).filter(User.email == data["email"]).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        email=data["email"],
        hashed_password=hash_password(data["password"])
    )

    db.add(user)
    db.commit()
    db.close()

    return {"message": "User created"}


@app.post("/login")
def login(data: dict):
    db = SessionLocal()

    user = db.query(User).filter(User.email == data["email"]).first()

    if not user or not verify_password(data["password"], user.hashed_password):
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"sub": user.email, "exp": datetime.utcnow() + timedelta(hours=2)},
        SECRET_KEY,
        algorithm="HS256"
    )

    db.close()

    return {"access_token": token}


# -------- ACTIVITIES --------
@app.get("/activities")
def get_activities(user=Depends(get_current_user)):
    activities = [clean(a) for a in core.get_user_activities(user.id)]
    return {"activities": activities}


@app.post("/activities")
def create_activity(activity: dict, user=Depends(get_current_user)):
    created = core.create_activity(
        activity["title"],
        activity["category"],
        activity["location"],
        activity.get("date"),
        activity["time"],
        user.id
    )
    return clean(created)


@app.delete("/activities/{activity_id}")
def delete_activity(activity_id: str, user=Depends(get_current_user)):
    core.delete_activity(activity_id)
    return {"status": "deleted"}


# -------- AI --------
@app.get("/ai/ask")
def ask_ai(q: str, user=Depends(get_current_user)):
    return {"answer": ai.ask_question(q)}


@app.get("/ai/summary")
def summary(user=Depends(get_current_user)):
    return {"summary": ai.summarize_activities()}