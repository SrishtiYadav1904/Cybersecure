import os
import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def get_auth_token():
    rand_user = f"inc_{uuid.uuid4().hex[:6]}"
    resp = client.post("/api/auth/register", json={
        "email": f"{rand_user}@test.com",
        "username": rand_user,
        "password": "Password123!",
        "role": "USER"
    })
    return resp.json()["access_token"]

def test_incident_lifecycle_and_report_generation():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Analyze text -> automatically initializes incident
    analysis_resp = client.post("/api/analyze/text", json={
        "text": "You are worthless and nobody likes you, go away.",
        "platform": "Twitter"
    }, headers=headers)
    assert analysis_resp.status_code == 200
    res_data = analysis_resp.json()
    incident_id = res_data["incident_id"]
    assert incident_id is not None

    # 2. Add second evidence under the SAME incident (CONTINUE flow)
    analysis_resp2 = client.post("/api/analyze/text", json={
        "text": "Second message: I will find you and hurt you.",
        "incident_id": incident_id,
        "platform": "Twitter"
    }, headers=headers)
    assert analysis_resp2.status_code == 200
    assert analysis_resp2.json()["incident_id"] == incident_id

    # 3. View incident details
    inc_resp = client.get(f"/api/incidents/{incident_id}", headers=headers)
    assert inc_resp.status_code == 200
    inc_data = inc_resp.json()
    assert inc_data["evidence_count"] >= 2

    # 4. Conclude incident & generate report (STOP flow)
    close_resp = client.post(f"/api/incidents/{incident_id}/close", headers=headers)
    assert close_resp.status_code == 200
    close_data = close_resp.json()
    assert "report_id" in close_data
    report_id = close_data["report_id"]

    # 5. Download report PDF
    dl_resp = client.get(f"/api/reports/{report_id}/download", headers=headers)
    assert dl_resp.status_code == 200
    assert dl_resp.headers["content-type"] == "application/pdf"
    assert len(dl_resp.content) > 1000 # Valid non-empty PDF bytes
