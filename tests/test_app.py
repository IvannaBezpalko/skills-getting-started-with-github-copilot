<<<<<<< HEAD
from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    original_participants = list(activities[activity_name]["participants"])

    try:
        participant = original_participants[0]
        response = client.delete(f"/activities/{activity_name}/participants/{participant}")

        assert response.status_code == 200
        assert participant not in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Removed {participant} from {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants
=======
import asyncio
import copy

import pytest
from httpx import ASGITransport, AsyncClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))


def make_request(method: str, path: str, **kwargs):
    async def run_request():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            request = getattr(client, method.lower())
            return await request(path, **kwargs)

    return asyncio.run(run_request())


def test_root_redirects_to_static_index():
    # Arrange
    # No special setup is required for this route.

    # Act
    response = make_request("get", "/")

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_seed_data():
    # Arrange
    # The in-memory activity database is loaded by the app module.

    # Act
    response = make_request("get", "/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"][0] == "michael@mergington.edu"


def test_signup_for_activity_adds_participant():
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = make_request(
        "post",
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_missing_activity_returns_404():
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = make_request(
        "post",
        "/activities/Unknown/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
>>>>>>> e18f688 (Add pytest as a dependency and implement tests for activity endpoints)
