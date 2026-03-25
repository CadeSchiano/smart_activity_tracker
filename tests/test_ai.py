from types import SimpleNamespace
from unittest.mock import patch

from apps import ai


def make_activity(
    title="Workout",
    category="Fitness",
    location="Gym",
    date="2026-03-20",
    time="09:00",
):
    return SimpleNamespace(
        title=title,
        category=category,
        location=location,
        date=date,
        time=time,
    )


@patch("apps.ai.client")
@patch("apps.ai.core.get_user_activities")
def test_ai_summary(mock_get_user_activities, mock_client):
    mock_get_user_activities.return_value = [make_activity()]
    mock_client.chat.completions.create.return_value.choices = [
        SimpleNamespace(message=SimpleNamespace(content="Mock summary"))
    ]

    result = ai.summarize_activities("user-123")

    assert result == "Mock summary"


@patch("apps.ai.client")
@patch("apps.ai.core.get_user_activities")
def test_ai_ask(mock_get_user_activities, mock_client):
    mock_get_user_activities.return_value = [make_activity(title="Study Session")]
    mock_client.chat.completions.create.return_value.choices = [
        SimpleNamespace(message=SimpleNamespace(content="Mock answer"))
    ]

    result = ai.ask_question("What activities do I have?", "user-123")

    assert result == "Mock answer"


@patch("apps.ai.client", None)
@patch("apps.ai.core.get_user_activities")
def test_ai_summary_fallback_without_api_key(mock_get_user_activities):
    mock_get_user_activities.return_value = [make_activity()]

    result = ai.summarize_activities("user-123")

    assert "You have 1 activities recorded." in result
    assert "Add an OpenAI API key" in result


@patch("apps.ai.client", None)
@patch("apps.ai.core.get_user_activities")
def test_ai_answer_fallback_without_api_key(mock_get_user_activities):
    mock_get_user_activities.return_value = [
        make_activity(title="Run Club", date="2026-03-20", time="07:00")
    ]

    result = ai.ask_question("What is my next activity?", "user-123")

    assert result == "Your next activity is Run Club on 2026-03-20 at 07:00."
