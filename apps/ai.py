from dotenv import load_dotenv
import os
from openai import OpenAI
from apps import core

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_activities():
    try:
        activities = core.get_all_activities()

        if not activities:
            return "No activities found."

        # Remove duplicates
        unique = set()
        clean_activities = []
        for a in activities:
            key = (a.title, a.category, a.location, a.date, a.time)
            if key not in unique:
                unique.add(key)
                clean_activities.append(a)

        activity_text = "\n".join([
            f"{a.title} ({a.category}) at {a.location} on {a.date} {a.time}"
            for a in clean_activities
        ])

        prompt = f"""
Summarize these activities clearly and briefly.

Rules:
- Do NOT repeat duplicate activities
- Keep it concise and readable

Activities:
{activity_text}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating summary: {str(e)}"


def ask_question(question: str):
    try:
        activities = core.get_all_activities()

        if not activities:
            return "No activities found."

        # Remove duplicates
        unique = set()
        clean_activities = []
        for a in activities:
            key = (a.title, a.category, a.location, a.date, a.time)
            if key not in unique:
                unique.add(key)
                clean_activities.append(a)

        activity_text = "\n".join([
            f"{a.title} ({a.category}) at {a.location} on {a.date} {a.time}"
            for a in clean_activities
        ])

        prompt = f"""
You are an assistant answering questions about user activities.

Rules:
- Do NOT repeat duplicate activities
- Be concise and clear
- Group similar activities if possible

Activities:
{activity_text}

Question:
{question}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error answering question: {str(e)}"