from unittest.mock import patch
from apps import ai, core


# Test summary function with mock
@patch("apps.ai.client.chat.completions.create")
def test_ai_summary(mock_openai):

    # Fake OpenAI response
    mock_openai.return_value.choices = [
        type("obj", (), {
            "message": type("msg", (), {"content": "Mock summary"})
        })
    ]

    # Add test data
    core.create_activity(
        title="Test Activity",
        category="Testing",
        location="Test Location",
        date="2026-03-20",
        time="10:00"
    )

    result = ai.summarize_activities()

    assert result == "Mock summary"


# Test ask_question function with mock
@patch("apps.ai.client.chat.completions.create")
def test_ai_ask(mock_openai):

    mock_openai.return_value.choices = [
        type("obj", (), {
            "message": type("msg", (), {"content": "Mock answer"})
        })
    ]

    core.create_activity(
        title="Another Test",
        category="Testing",
        location="Lab",
        date="2026-03-21",
        time="12:00"
    )

    result = ai.ask_question("What activities do I have?")

    assert result == "Mock answer"