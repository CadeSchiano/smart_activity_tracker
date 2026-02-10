import pytest
from apps import core

@pytest.fixture(autouse=True)
def clear_state():
    core.activities.clear()

def test_create_activity():
    core.create_activity(
        "Gym",
        "Fitness",
        "Rec Center",
        "2024-10-02",
        "18:00"
    )

    assert len(core.activities) == 1
    assert core.activities[0].date == "2024-10-02"

def test_list_activities():
    core.create_activity("Run", "Fitness", "Park", "2024-10-02", "07:00")

    summaries = core.list_activities()
    assert len(summaries) == 1
    assert "Run (Fitness)" in summaries[0]
