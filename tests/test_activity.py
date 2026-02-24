import pytest
from apps.activity import Activity


def test_activity_creation():
    activity = Activity(
        title="Hiking",
        category="Outdoor",
        location="Trail",
        date="2024-10-02",
        time="09:00"
    )

    assert activity.title == "Hiking"
    assert activity.date == "2024-10-02"


def test_activity_summary():
    activity = Activity(
        title="Yoga",
        category="Wellness",
        location="Studio",
        date="2024-10-03",
        time="10:00"
    )

    summary = activity.to_dict()

    assert summary["title"] == "Yoga"
    assert summary["category"] == "Wellness"
