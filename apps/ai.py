import os
from collections import Counter

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    def load_dotenv():
        return False

from openai import OpenAI

from apps import core

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def _get_user_activities(user_id):
    activities = core.get_user_activities(user_id)

    unique = set()
    clean_activities = []
    for activity in activities:
      key = (
          activity.title,
          activity.category,
          activity.location,
          activity.date,
          activity.time,
      )
      if key not in unique:
          unique.add(key)
          clean_activities.append(activity)

    return clean_activities


def _activity_lines(activities):
    return [
        f"{a.title} ({a.category}) at {a.location} on {a.date} {a.time}"
        for a in activities
    ]


def _fallback_summary(activities):
    categories = Counter(a.category for a in activities if a.category)
    upcoming = sorted(
        activities,
        key=lambda a: ((a.date or "9999-99-99"), (a.time or "99:99")),
    )
    category_text = ", ".join(
        f"{category}: {count}" for category, count in categories.most_common(3)
    )
    next_item = upcoming[0]

    parts = [f"You have {len(activities)} activities recorded."]
    if category_text:
        parts.append(f"Top categories: {category_text}.")
    parts.append(
        f"Next activity: {next_item.title} on {next_item.date or 'an unscheduled date'} at {next_item.time or 'an unscheduled time'}."
    )
    parts.append("Add an OpenAI API key to enable richer AI responses.")
    return " ".join(parts)


def _fallback_answer(question, activities):
    lowered = question.lower()

    if "next" in lowered:
        next_item = sorted(
            activities,
            key=lambda a: ((a.date or "9999-99-99"), (a.time or "99:99")),
        )[0]
        return (
            f"Your next activity is {next_item.title} on "
            f"{next_item.date or 'an unscheduled date'} at {next_item.time or 'an unscheduled time'}."
        )

    if "where" in lowered:
        locations = [a.location for a in activities if a.location]
        if locations:
            return f"Your activities are scheduled across: {', '.join(sorted(set(locations)))}."

    return _fallback_summary(activities)


def summarize_activities(user_id):
    activities = _get_user_activities(user_id)

    if not activities:
        return "No activities found."

    if not client:
        return _fallback_summary(activities)

    activity_text = "\n".join(_activity_lines(activities))
    prompt = f"""
Summarize these activities clearly and briefly.

Rules:
- Do not repeat duplicate activities.
- Keep it concise and readable.
- Mention the most important patterns, upcoming items, and category mix.

Activities:
{activity_text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You summarize a user's activity schedule in a concise, practical way.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as error:
        return f"Error generating summary: {error}"


def ask_question(question: str, user_id):
    activities = _get_user_activities(user_id)

    if not activities:
        return "No activities found."

    if not client:
        return _fallback_answer(question, activities)

    activity_text = "\n".join(_activity_lines(activities))
    prompt = f"""
You are an assistant answering questions about a user's activities.

Rules:
- Do not repeat duplicate activities.
- Be concise and clear.
- Answer only from the provided activities.
- If the answer is not in the activities, say so plainly.

Activities:
{activity_text}

Question:
{question}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You answer questions about a user's schedule and activities using only the given data.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as error:
        return f"Error answering question: {error}"
