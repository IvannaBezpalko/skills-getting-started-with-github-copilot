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
