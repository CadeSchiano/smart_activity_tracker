"""
core.py

This file contains the core logic for handling activities.
No web code, no database code — just Python logic.
"""

import json
from pathlib import Path
from . import activity

# -------------------------
# Data storage
# -------------------------

DATA_FILE = Path("data/activities.json")
activities = []

# -------------------------


# -------------------------

def load_activities():
    """
    Load activities from the JSON data file.
    """
    activities.clear()

    if not DATA_FILE.exists():
        return

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    for item in data:
        act = activity.Activity(
            title=item["title"],
            category=item["category"],
            location=item["location"],
            time=item["time"]
        )
        activities.append(act)


def save_activities():
    """
    Save activities to the JSON data file.
    """
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w") as file:
        json.dump(
            [act.to_dict() for act in activities],
            file,
            indent=2
        )

# -------------------------
# Core functions
# -------------------------

def create_activity(title: str, category: str, location: str, time: str):
    """
    Add a new activity to the activities list.
    """
    new_activity = activity.Activity(title, category, location, time)
    activities.append(new_activity)
    save_activities()


def list_activities():
    """
    Return a list of activity summaries.
    """
    return [act.summary() for act in activities]


def find_activities_by_category(category: str):
    """
    Find activities by category.
    """
    return [act for act in activities if act.category == category]

def has_activities() -> bool:
    """
    Return True if there are any activities loaded.
    """
    return len(activities) > 0


# -------------------------
# Startup
# -------------------------

load_activities()
