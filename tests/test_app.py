from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    original_participants = list(activities[activity_name]["participants"])
    duplicate_email = original_participants[0]

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": duplicate_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"
    assert activities[activity_name]["participants"] == original_participants


def test_unregister_participant_removes_them_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    activities[activity_name]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert response.status_code == 200

    delete_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    assert delete_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert delete_response.json()["message"] == f"Unregistered {email} from {activity_name}"
