import os
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, Field, field_validator

from apps.database import Base, engine, SessionLocal
from apps.models import User
from apps.auth import hash_password, verify_password
from apps import core, ai
from apps.rate_limit import enforce_rate_limit

app = FastAPI()

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOW_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

Base.metadata.create_all(bind=engine)

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
if len(SECRET_KEY) < 32:
    raise RuntimeError("JWT_SECRET_KEY must be set to a random value of at least 32 characters.")

ACCESS_TOKEN_TTL_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

Email = Annotated[str, Field(min_length=3, max_length=254)]
Password = Annotated[str, Field(min_length=8, max_length=128)]
ActivityText = Annotated[str, Field(min_length=1, max_length=200)]


class Credentials(BaseModel):
    email: Email
    password: Password

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        email = value.strip().lower()
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            raise ValueError("Enter a valid email address.")
        return email


class ActivityCreate(BaseModel):
    title: ActivityText
    category: ActivityText
    location: Annotated[str, Field(min_length=1, max_length=300)]
    date: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$")]
    time: Annotated[str, Field(pattern=r"^\d{2}:\d{2}$")]

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError as error:
            raise ValueError("Enter a valid date.") from error
        return value

    @field_validator("time")
    @classmethod
    def validate_time(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%H:%M")
        except ValueError as error:
            raise ValueError("Enter a valid time.") from error
        return value


class AiQuestion(BaseModel):
    q: Annotated[str, Field(min_length=1, max_length=1_000)]


# -------- CLEAN RESPONSE --------
def clean(obj):
    return {
        "id": obj.id,
        "title": obj.title,
        "category": obj.category,
        "location": obj.location,
        "date": obj.date,
        "time": obj.time,
    }


# -------- AUTH --------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")

        if not isinstance(user_id, str):
            raise HTTPException(status_code=401, detail="Invalid token")

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=401, detail="Invalid user")
            return user
        finally:
            db.close()

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def request_client_key(request: Request) -> str:
    return request.client.host if request.client else "unknown"


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: Credentials, request: Request):
    enforce_rate_limit("register", request_client_key(request), limit=5, window_seconds=3600)
    db = SessionLocal()

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Unable to create an account with these details")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.close()

    return {"message": "User created"}


@app.post("/login")
def login(data: Credentials, request: Request):
    enforce_rate_limit("login", request_client_key(request), limit=10, window_seconds=900)
    db = SessionLocal()

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {
            "sub": user.id,
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_TTL_MINUTES),
        },
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
def create_activity(activity: ActivityCreate, user=Depends(get_current_user)):
    created = core.create_activity(
        activity.title,
        activity.category,
        activity.location,
        activity.date,
        activity.time,
        user.id
    )
    return clean(created)


@app.delete("/activities/{activity_id}")
def delete_activity(activity_id: str, user=Depends(get_current_user)):
    if not core.delete_activity(activity_id, user.id):
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"status": "deleted"}


# -------- AI --------
@app.post("/ai/ask")
def ask_ai(question: AiQuestion, user=Depends(get_current_user)):
    enforce_rate_limit("ai", user.id, limit=20, window_seconds=3600)
    return {"answer": ai.ask_question(question.q, user.id)}


@app.get("/ai/summary")
def summary(user=Depends(get_current_user)):
    enforce_rate_limit("ai", user.id, limit=20, window_seconds=3600)
    return {"summary": ai.summarize_activities(user.id)}
