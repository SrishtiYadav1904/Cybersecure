import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.auth.security import get_password_hash, verify_password, create_access_token, decode_access_token

client = TestClient(app)

def test_password_hashing():
    pw = "SecureTestPassword123!"
    h = get_password_hash(pw)
    assert h != pw
    assert verify_password(pw, h) is True
    assert verify_password("WrongPassword", h) is False

def test_jwt_token_creation_and_decoding():
    payload = {"sub": "123", "role": "USER"}
    token = create_access_token(payload)
    assert isinstance(token, str)
    assert len(token) > 20
    decoded = decode_access_token(token)
    assert decoded["sub"] == "123"
    assert decoded["role"] == "USER"

def test_user_registration_and_login():
    import uuid
    rand_user = f"test_{uuid.uuid4().hex[:6]}"
    email = f"{rand_user}@example.com"
    pw = "CyberGuard2026!Pass"

    # Register
    reg_resp = client.post("/api/auth/register", json={
        "email": email,
        "username": rand_user,
        "password": pw,
        "full_name": "Test User",
        "role": "USER"
    })
    assert reg_resp.status_code == 201
    data = reg_resp.json()
    assert "access_token" in data
    assert data["user"]["email"] == email

    # Login
    login_resp = client.post("/api/auth/login", json={
        "email": email,
        "password": pw
    })
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert "access_token" in login_data
    token = login_data["access_token"]

    # Profile Me
    me_resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["username"] == rand_user
