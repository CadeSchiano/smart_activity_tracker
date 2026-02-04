# Main application file for managing activities
from apps import core


def main():

    # STEP 1: Only create demo activities if none exist
    if not core.has_activities():
        print("No activities found. Starting fresh.")

        core.create_activity("Hiking", "Outdoor", "Mountain Trail", "2024-08-01 09:00")
        core.create_activity("Cooking Class", "Indoor", "Community Center", "2024-08-05 18:00")
        core.create_activity("Bird Watching", "Outdoor", "Nature Reserve", "2024-08-10 07:00")

    else:
        print("Activities loaded successfully.")

    # STEP 2: Always list activities
    summaries = core.list_activities()

    print("Activities:")
    for summary in summaries:
        print(f"- {summary}")


if __name__ == "__main__":
    main()
