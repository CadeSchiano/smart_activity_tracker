"""
core.py

This file contains the core logic for handling activities.
No web code, no database code — just Python logic.
"""

# -------------------------
# Data storage
# -------------------------

# This will hold all activities
activities = []


# -------------------------
# Functions
# -------------------------

def create_activity(title, category, location, time):
    
    activity = {
        'title': title,
        'category': category,
        'location': location,
        'time': time
    }
    activities.append(activity)
    


# -------------------------
# Listing activities
# -------------------------
def list_activities():
    """
    List all activities in a readable format.
    """
    for activity in activities:
        print(f"Title: {activity['title']}")
        print(f"Category: {activity['category']}")
        print(f"Location: {activity['location']}")
        print(f"Time: {activity['time']}")
        print("-" * 20)




