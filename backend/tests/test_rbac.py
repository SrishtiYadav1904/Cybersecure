import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.session import SessionLocal
from backend.app.database.models import User
from backend.app.auth.security import get_password_hash, create_access_token

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_rbac_users():
    db = SessionLocal()
    # Create or update test users with distinct roles
    users = [
        ("rbac_user@test.com", "user123", "Regular User", "USER"),
        ("rbac_admin@test.com", "admin123", "Admin User", "ADMIN"),
        ("rbac_consultant@test.com", "cons123", "Consultant User", "CONSULTANT")
    ]
    created = {}
    for email, pwd, name, role in users:
        u = db.query(User).filter(User.email == email).first()
        if not u:
            u = User(
                email=email,
                username=email.split("@")[0],
                full_name=name,
                hashed_password=get_password_hash(pwd),
                role=role,
                is_active=True
            )
            db.add(u)
            db.commit()
            db.refresh(u)
        else:
            u.role = role
            db.commit()
            db.refresh(u)
        token = create_access_token({"sub": str(u.id), "role": u.role})
        created[role] = token
    db.close()
    return created

def test_user_cannot_access_admin_dashboard(setup_rbac_users):
    """USER must receive 403 Forbidden on admin endpoints."""
    user_token = setup_rbac_users["USER"]
    resp = client.get("/api/admin/dashboard", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 403, f"Expected 403 for USER on admin dashboard, got {resp.status_code}"
    assert "Access denied" in resp.json()["detail"]

def test_user_cannot_access_consultant_cases(setup_rbac_users):
    """USER must receive 403 Forbidden on consultant endpoints."""
    user_token = setup_rbac_users["USER"]
    resp = client.get("/api/help-request/cases", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 403, f"Expected 403 for USER on consultant cases, got {resp.status_code}"

def test_admin_cannot_access_consultant_cases(setup_rbac_users):
    """ADMIN must receive 403 Forbidden on consultant-only endpoints unless certified."""
    admin_token = setup_rbac_users["ADMIN"]
    resp = client.get("/api/help-request/cases", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 403, f"Expected 403 for ADMIN on consultant cases, got {resp.status_code}"

def test_admin_can_access_admin_dashboard(setup_rbac_users):
    """ADMIN must successfully access admin dashboard."""
    admin_token = setup_rbac_users["ADMIN"]
    resp = client.get("/api/admin/dashboard", headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 200

def test_consultant_can_access_consultant_cases(setup_rbac_users):
    """CONSULTANT must successfully access escalated cases."""
    cons_token = setup_rbac_users["CONSULTANT"]
    resp = client.get("/api/help-request/cases", headers={"Authorization": f"Bearer {cons_token}"})
    assert resp.status_code == 200
