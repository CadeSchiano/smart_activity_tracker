"""
core.py

Core business logic and persistence.
No FastAPI or UI code.
"""

import json
from pathlib import Path
from .activity import Activity

# -------------------------
# Data storage
# -------------------------

DATA_FILE = Path("data/activities.json")
activities = []

# -------------------------
# Persistence
# -------------------------

def load_activities():
    activities.clear()

    if not DATA_FILE.exists():
        return

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return

    for item in data:
        activities.append(
            Activity(
                id=item["id"],
                title=item["title"],
                category=item["category"],
                location=item["location"],
                date=item["date"],
                time=item["time"]
            )
        )


def save_activities():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w") as file:
        json.dump([a.to_dict() for a in activities], file, indent=2)

# -------------------------
# Core API
# -------------------------

def create_activity(title: str, category: str, location: str, date: str, time: str):
    activity = Activity(title, category, location, date, time)
    activities.append(activity)
    save_activities()
    return activity


def list_activities():
    return [a.summary() for a in activities]


def find_activities_by_category(category: str):
    return [a for a in activities if a.category == category]


def has_activities() -> bool:
    return len(activities) > 0

def get_activity_by_id(activity_id: str) -> Activity:
    for activity in activities:
        if activity.id == activity_id:
            return activity
    return None

def delete_activity(activity_id: str) -> bool:
    global activities
    original_count = len(activities)
    activities = [a for a in activities if a.id != activity_id]
    if len(activities) < original_count:
        save_activities()
        return True
    return False

def get_all_activities():
    return list(activities)


# -------------------------
# Startup
# -------------------------

load_activities()
