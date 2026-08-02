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
import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))


@pytest.fixture
def client():
    with TestClient(app, follow_redirects=False) as test_client:
        yield test_client


def test_root_redirects_to_static_index(client):
    # Arrange
    # No special setup is required for this route.

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_seed_data(client):
    # Arrange
    # The in-memory activity database is loaded by the app module.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"][0] == "michael@mergington.edu"


def test_signup_for_activity_adds_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_missing_activity_returns_404(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        "/activities/Unknown/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
>>>>>>> e18f688 (Add pytest as a dependency and implement tests for activity endpoints)
