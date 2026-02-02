import pytest
from apps.activity import Activity


def test_activity_creation_valid():
    activity = Activity(
        title = "Hiking",
        category = "Outdoor",
        location = "Mountain Trail",
        time = "2024-08-01 09:00"
    )

    assert activity.title == "Hiking"
    assert activity.category == "Outdoor"
    assert activity.location == "Mountain Trail"
    assert activity.time == "2024-08-01 09:00"

def test_activity_creation_missing_fields():
    with pytest.raises(ValueError) as excinfo:
        activity = Activity(
            title = "Hiking",
            category = "",
            location = "Mountain Trail",
            time = "2024-08-01 09:00"
        )
    assert "All activity fields must be provided." in str(excinfo.value)

def test_activity_summary():
    activity = Activity(
        title = "Yoga Class",
        category = "Wellness",
        location = "Studio A",
        time = "2024-08-05 10:00"
    )

    summary = activity.summary()
    expected_summary = "Yoga Class (Wellness) at Studio A on 2024-08-05 10:00"
    assert summary == expected_summary