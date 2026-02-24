import pytest
from apps import core


def test_create_and_list():
    activity = core.create_activity(
        title="Core Test",
        category="Testing",
        location="Lab",
        date="2026-03-01",
        time="12:00"
    )

    assert activity.title == "Core Test"

    all_activities = core.get_all_activities()
    assert len(all_activities) >= 1
