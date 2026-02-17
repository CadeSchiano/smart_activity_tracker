import pytest
from apps.activity import Activity

def test_activity_creation_valid():
    activity = Activity(
        title="Hiking",
        category="Outdoor",
        location="Trail",
        date="2024-10-02",
        time="09:00"
    )

    assert activity.date == "2024-10-02"
    assert activity.time == "09:00"

def test_activity_missing_fields():
    with pytest.raises(ValueError):
        Activity(
            title="",
            category="Outdoor",
            location="Trail",
            date="2024-10-02",
            time="09:00"
        )

def test_activity_summary():
    activity = Activity(
        "Yoga", "Wellness", "Studio", "2024-10-03", "10:00"
    )

    summary = activity.summary()
    assert "Yoga (Wellness) at Studio on 2024-10-03 at 10:00" in summary

