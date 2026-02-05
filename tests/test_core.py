import pytest
from apps import core
from apps import activity

@pytest.fixture(autouse=True)
def clear_activities():
    core.activities.clear()

def test_create_activity_adds_activity():
    activity = core.create_activity(
        title="Hiking",
        category="Outdoor",
        location="Mountain Trail",
        time="2024-08-01 09:00"
    )
    assert len(core.activities) == 1
    assert core.activities[0].title == "Hiking"

def test_list_activities_returns_summaries():
    core.create_activity("Hiking", "Outdoor", "Mountain Trail", "2024-08-01 09:00")
    core.create_activity("Cooking Class", "Indoor", "Community Center", "2024-08-05 18:00")

    summaries = core.list_activities()
    assert len(summaries) == 2
    assert summaries[0] == "Hiking (Outdoor) at Mountain Trail on 2024-08-01 09:00"
    assert summaries[1] == "Cooking Class (Indoor) at Community Center on 2024-08-05 18:00"

def test_find_activities_by_category():
    core.create_activity("Hiking", "Outdoor", "Mountain Trail", "2024-08-01 09:00")
    core.create_activity("Cooking Class", "Indoor", "Community Center", "2024-08-05 18:00")
    core.create_activity("Bird Watching", "Outdoor", "Nature Reserve", "2024-08-10 07:00")

    outdoor_activities = core.find_activities_by_category("Outdoor")
    assert len(outdoor_activities) == 2
    assert all(act.category == "Outdoor" for act in outdoor_activities)

def test_has_activities():
    assert not core.has_activities()
    core.create_activity("Hiking", "Outdoor", "Mountain Trail", "2024-08-01 09:00")
    assert core.has_activities()