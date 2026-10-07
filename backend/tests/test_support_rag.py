import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def get_auth_token():
    rand_user = f"sup_{uuid.uuid4().hex[:6]}"
    resp = client.post("/api/auth/register", json={
        "email": f"{rand_user}@test.com",
        "username": rand_user,
        "password": "Password123!",
        "role": "USER"
    })
    return resp.json()["access_token"]

def test_support_session_and_rag():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Start session
    start_resp = client.post("/api/support/start", headers=headers)
    assert start_resp.status_code == 200
    session_data = start_resp.json()
    session_id = session_data["id"]

    # Send blocking query (Triggers RAG retrieval)
    msg_resp = client.post("/api/support/message", json={
        "session_id": session_id,
        "message": "How do I block someone on Instagram who is threatening me?"
    }, headers=headers)
    assert msg_resp.status_code == 200
    msg_data = msg_resp.json()
    assert msg_data["sender"] == "assistant"
    # Verify no diagnostic violations
    assert "you have depression" not in msg_data["content"].lower()
    assert "you are mentally ill" not in msg_data["content"].lower()

    # Verify Emergency resources endpoint
    res_resp = client.get("/api/support/resources")
    assert res_resp.status_code == 200
    resources = res_resp.json()
    assert len(resources) > 0
    helpline_numbers = [r.get("contact_number") for r in resources]
    assert any("1930" in str(num) for num in helpline_numbers)
