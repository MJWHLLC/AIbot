import os
import sys
import pytest

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, model_client
from users import create_user, generate_token, validate_token


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["MAIL_BACKEND"] = "testing"  # Disable real email in tests
    with app.test_client() as client:
        yield client


def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Paralegal AI Assistant" in rv.data


def test_ask_mock(client, monkeypatch):
    # Ensure model client runs in mock mode by removing token env var
    monkeypatch.delenv("GITHUB_MODEL_API_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_MODEL_NAME", raising=False)
    monkeypatch.delenv("AUTH_USERNAME", raising=False)
    
    # Login first (auth is disabled when AUTH_USERNAME is not set)
    rv = client.post(
        "/login",
        data={"username": "testuser", "password": ""},
        follow_redirects=True
    )
    assert rv.status_code == 200

    rv = client.post(
        "/ask",
        data={"query": "Draft a basic complaint checklist", "document_type": "Complaint", "jurisdiction": "Federal"},
        follow_redirects=True,
    )
    assert rv.status_code == 200
    assert b"MOCK RESPONSE" in rv.data or b"mocked" in rv.data.lower()


def test_invite_flow(client):
    """Test the invite flow: admin creates invite, user signs up."""
    # Create an admin user
    create_user("admin", "AdminPass123", is_admin=True)
    
    # Login as admin
    rv = client.post(
        "/login",
        data={"username": "admin", "password": "AdminPass123"},
        follow_redirects=True
    )
    assert rv.status_code == 200
    
    # Admin generates an invite for a new user
    rv = client.post("/admin/invite", data={"username": "newuser", "email": "newuser@example.com"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Invite sent" in rv.data or b"invite" in rv.data.lower()
    
    # Generate a token directly for testing
    token = generate_token("testuser", "invite", expires_in_hours=72)
    
    # User visits the join page
    rv = client.get(f"/join?token={token}")
    assert rv.status_code == 200
    assert b"Create Account" in rv.data
    
    # User completes signup
    rv = client.post(
        "/join",
        data={"token": token, "password": "UserPass123", "confirm": "UserPass123"},
        follow_redirects=True
    )
    assert rv.status_code == 200
    assert b"successfully" in rv.data or b"login" in rv.data


def test_password_reset_flow(client):
    """Test the password-reset flow."""
    # Create a user
    create_user("testuser", "OldPassword123", is_admin=False)
    
    # User visits reset page
    rv = client.get("/reset")
    assert rv.status_code == 200
    assert b"Reset Password Request" in rv.data
    
    # Generate a reset token for testing
    token = generate_token("testuser", "password_reset", expires_in_hours=1)
    
    # Validate the token
    username = validate_token(token, "password_reset")
    assert username == "testuser"
    
    # User visits the reset page
    rv = client.get(f"/reset-password?token={token}")
    assert rv.status_code == 200
    assert b"Reset Password" in rv.data
    
    # User sets a new password
    rv = client.post(
        "/reset-password",
        data={"token": token, "password": "NewPassword123", "confirm": "NewPassword123"},
        follow_redirects=True
    )
    assert rv.status_code == 200
    assert b"successfully" in rv.data or b"login" in rv.data
