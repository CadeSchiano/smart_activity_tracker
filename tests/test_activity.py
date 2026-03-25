import pytest
from apps.activity import Activity


def test_activity_creation():
    activity = Activity(
        title="Hiking",
        category="Outdoor",
        location="Trail",
        date="2024-10-02",
        time="09:00",
        user_id="user-1",
    )

    assert activity.title == "Hiking"
    assert activity.date == "2024-10-02"
    assert activity.user_id == "user-1"


def test_activity_summary():
    activity = Activity(
        title="Yoga",
        category="Wellness",
        location="Studio",
        date="2024-10-03",
        time="10:00",
        user_id="user-2",
    )

    summary = activity.to_dict()

    assert summary["title"] == "Yoga"
    assert summary["category"] == "Wellness"
    assert summary["user_id"] == "user-2"
