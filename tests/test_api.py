from fastapi.testclient import TestClient

from apps.api import app

client = TestClient(app)


def auth_headers(email="api-test@example.com", password="secret123"):
    register_response = client.post(
        "/register",
        json={"email": email, "password": password},
    )
    assert register_response.status_code == 200

    login_response = client.post(
        "/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_full_activity_lifecycle():
    headers = auth_headers()

    post_response = client.post(
        "/activities",
        headers=headers,
        json={
            "title": "API Test",
            "category": "Testing",
            "location": "Test Suite",
            "date": "2026-03-01",
            "time": "12:00",
        },
    )

    assert post_response.status_code == 200
    created = post_response.json()
    assert created["title"] == "API Test"

    activity_id = created["id"]

    get_all_response = client.get("/activities", headers=headers)
    assert get_all_response.status_code == 200
    assert len(get_all_response.json()["activities"]) == 1

    delete_response = client.delete(f"/activities/{activity_id}", headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json() == {"status": "deleted"}

    get_after_delete_response = client.get("/activities", headers=headers)
    assert get_after_delete_response.status_code == 200
    assert get_after_delete_response.json()["activities"] == []


def test_ai_endpoints_require_auth_and_return_data():
    headers = auth_headers(email="ai-api@example.com")

    client.post(
        "/activities",
        headers=headers,
        json={
            "title": "Run Club",
            "category": "Fitness",
            "location": "Park",
            "date": "2026-03-02",
            "time": "08:00",
        },
    )

    summary_response = client.get("/ai/summary", headers=headers)
    assert summary_response.status_code == 200
    assert "summary" in summary_response.json()

    ask_response = client.get("/ai/ask", headers=headers, params={"q": "What is my next activity?"})
    assert ask_response.status_code == 200
    assert "answer" in ask_response.json()


def test_protected_routes_reject_missing_token():
    response = client.get("/activities")
    assert response.status_code == 401
