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
    return activity

def add_activity(activity):
    """
    Add an activity to the activities list.
    """
    activities.append(activity)
    return activity
    pass


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



# -------------------------
# Script execution
# -------------------------

def main():
    #Example

    create_activity("Hiking", "Outdoor", "Mountain Trail", "2024-07-15 08:00")
    create_activity("Cooking Class", "Indoor", "Community Center", "2024-07-16 18:00")
    list_activities()

if __name__ == "__main__":
    main()