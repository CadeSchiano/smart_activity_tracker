"""
core.py

This file contains the core logic for handling activities.
No web code, no database code — just Python logic.
"""

# -------------------------
# Data storage
# -------------------------
from apps import activity


activities = []


# -------------------------
# Functions
# -------------------------




def create_activity(title: str, category: str, location: str, time: str):
    """
    Add a new activity to the activities list.
    """
    new_activity = activity.Activity(title, category, location, time)
    activities.append(new_activity)
    




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
