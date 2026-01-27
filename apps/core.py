"""
core.py

This file contains the core logic for handling activities.
No web code, no database code — just Python logic.
"""

# -------------------------
# Data storage
# -------------------------
import activity

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
    List all activities in a readable format.
    """
    print("Activities:")
    for activity in activities:
        print(f"Title: {activity.title}")
        print(f"Category: {activity.category}")
        print(f"Location: {activity.location}")
        print(f"Time: {activity.time}")
        print("-" * 20)
