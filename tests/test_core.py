from apps import core


def test_create_get_and_delete_user_activity():
    user_id = "core-user-1"

    activity = core.create_activity(
        title="Core Test",
        category="Testing",
        location="Lab",
        date="2026-03-01",
        time="12:00",
        user_id=user_id,
    )

    assert activity.title == "Core Test"
    assert activity.user_id == user_id

    all_activities = core.get_user_activities(user_id)
    assert len(all_activities) == 1
    assert all_activities[0].title == "Core Test"

    core.delete_activity(activity.id)
    assert core.get_user_activities(user_id) == []


def test_get_user_activities_is_user_scoped():
    first_user = "user-a"
    second_user = "user-b"

    core.create_activity("A", "Work", "Office", "2026-03-01", "09:00", first_user)
    core.create_activity("B", "Gym", "Studio", "2026-03-02", "18:00", second_user)

    first_user_activities = core.get_user_activities(first_user)
    second_user_activities = core.get_user_activities(second_user)

    assert len(first_user_activities) == 1
    assert len(second_user_activities) == 1
    assert first_user_activities[0].title == "A"
    assert second_user_activities[0].title == "B"
