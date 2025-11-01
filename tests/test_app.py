"""
Tests for the FastAPI application.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

@pytest.fixture
def test_activities():
    """Sample activities data for testing"""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        }
    }

def test_get_activities():
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    # Ensure some key fields are present in the response
    for activity in response.json().values():
        assert all(key in activity for key in ["description", "schedule", "max_participants", "participants"])

def test_signup_new_participant():
    """Test signing up a new participant for an activity"""
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    
    # Verify the student was added
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]

def test_signup_duplicate_participant():
    """Test signing up a participant who is already registered"""
    email = "michael@mergington.edu"  # This email is already in Chess Club
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity():
    """Test signing up for an activity that doesn't exist"""
    email = "student@mergington.edu"
    response = client.post(f"/activities/NonexistentClub/signup?email={email}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]