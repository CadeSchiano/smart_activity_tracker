import pytest
from fastapi.testclient import TestClient
from apps.api import app

client = TestClient(app)


def test_full_activity_lifecycle():
    # -------------------------
    # CREATE (POST)
    # -------------------------
    post_response = client.post(
        "/activities",
        json={
            "title": "API Test",
            "category": "Testing",
            "location": "Test Suite",
            "date": "2026-03-01",
            "time": "12:00"
        }
    )

    assert post_response.status_code == 201
    created = post_response.json()
    assert created["title"] == "API Test"

    activity_id = created["id"]


    # -------------------------
    # GET ALL
    # -------------------------
    get_all_response = client.get("/activities")
    assert get_all_response.status_code == 200
    assert get_all_response.json()["count"] >= 1


    # -------------------------
    # GET BY ID
    # -------------------------
    get_one_response = client.get(f"/activities/{activity_id}")
    assert get_one_response.status_code == 200
    assert get_one_response.json()["id"] == activity_id


    # -------------------------
    # DELETE
    # -------------------------
    delete_response = client.delete(f"/activities/{activity_id}")
    assert delete_response.status_code == 200


    # -------------------------
    # VERIFY DELETED
    # -------------------------
    get_deleted = client.get(f"/activities/{activity_id}")
    assert get_deleted.status_code == 404
