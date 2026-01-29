# Main application file for managing activities
import core



def main():

    
    # Create some activities
    activity1 = core.create_activity("Jogging", "Outdoor", "Park", "2024-07-15 08:00")
    activity2 = core.create_activity("Cooking Class", "Indoor", "Community Center", "2024-07-20 18:00")
    activity3 = core.create_activity("Book Club", "Social", "Library", "2024-07-22 19:00")
    activity4 = core.create_activity("Rocket League Tournament", "Gaming", "Online", "2024-07-25 20:00")
    
    summaries = core.list_activities()

    print("Activities:")
    for summary in summaries:
        print(f"- {summary}")


# Run the main function
if __name__ == "__main__":
    main()

