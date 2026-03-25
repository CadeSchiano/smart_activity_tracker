from apps import ai, core

DEMO_USER_ID = "demo-user"


def seed_demo_activities():
    if core.get_user_activities(DEMO_USER_ID):
        return

    core.create_activity("Hiking", "Outdoor", "Mountain Trail", "2026-04-01", "09:00", DEMO_USER_ID)
    core.create_activity("Cooking Class", "Indoor", "Community Center", "2026-04-05", "18:00", DEMO_USER_ID)
    core.create_activity("Bird Watching", "Outdoor", "Nature Reserve", "2026-04-10", "07:00", DEMO_USER_ID)


def main():
    seed_demo_activities()

    activities = core.get_user_activities(DEMO_USER_ID)
    print("Demo activities:")
    for activity in activities:
        print(
            f"- {activity.title} ({activity.category}) at {activity.location} "
            f"on {activity.date} {activity.time}"
        )

    print()
    print("AI summary:")
    print(ai.summarize_activities(DEMO_USER_ID))


if __name__ == "__main__":
    main()
