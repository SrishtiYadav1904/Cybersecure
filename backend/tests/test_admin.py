from fastapi.testclient import TestClient
from backend.app.main import app

def test_admin_dashboard_and_monitoring():
    with TestClient(app) as client:
        # Login as seeded default Admin
        login_resp = client.post("/api/auth/login", json={
            "email": "admin@cyberguard.ai",
            "password": "AdminSecure2026!"
        })
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Dashboard metrics
        dash_resp = client.get("/api/admin/dashboard", headers=headers)
        assert dash_resp.status_code == 200
        stats = dash_resp.json()
        assert "total_users" in stats
        assert "current_model_version" in stats
        assert "drift_status" in stats

        # Model monitoring
        models_resp = client.get("/api/admin/models", headers=headers)
        assert models_resp.status_code == 200
        models = models_resp.json()
        assert len(models) >= 1
        assert models[0]["version_tag"] == "CB-RO-001"

        # Drift endpoint
        drift_resp = client.get("/api/admin/drift", headers=headers)
        assert drift_resp.status_code == 200
        drift_data = drift_resp.json()
        assert "psi_value" in drift_data
