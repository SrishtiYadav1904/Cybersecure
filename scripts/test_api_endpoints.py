import urllib.request
import json
import sys

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_auth_token():
    login_url = "http://127.0.0.1:8000/api/auth/login"
    login_data = json.dumps({"email": "rbac_user@test.com", "password": "user123"}).encode("utf-8")
    req = urllib.request.Request(login_url, data=login_data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["access_token"]
    except urllib.error.HTTPError:
        # If user does not exist, register them
        reg_url = "http://127.0.0.1:8000/api/auth/register"
        reg_data = json.dumps({
            "email": "rbac_user@test.com",
            "password": "user123",
            "full_name": "Test User",
            "role": "USER"
        }).encode("utf-8")
        reg_req = urllib.request.Request(reg_url, data=reg_data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(reg_req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["access_token"]

def test_api():
    token = get_auth_token()
    print(f"Authenticated successfully! Token acquired.\n")

    tests = [
        "I will rape you",
        "moti bhaisn marr jaa",
        "tu chutiya hai",
        "tu bahut gandi hai",
        "mar ja",
        "main tujhe maar dunga",
        "घर से बाहर निकल, तुझे जान से मार दूंगा आज।",
        "Thank you so much for explaining the code, really helpful project!",
        "Bhai project submit ho gaya, thanks for helping me out yaar!"
    ]

    print("=== Testing FastAPI /api/analyze/text End-to-End ===\n")
    for t in tests:
        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/analyze/text",
            data=json.dumps({"text": t}).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"Query:      \"{t}\"")
            print(f"Prediction: {data['predicted_class']} (Cyberbullying: {data['is_cyberbullying']}, Severity: {data.get('severity')})")
            print(f"Confidence: {data['confidence'] * 100:.2f}% | Lang: {data.get('detected_language')}")
            top3 = [(p['category'], round(p['probability'], 3)) for p in data.get('probabilities', [])[:3]]
            print(f"Top-3:      {top3}")
            print("-" * 60)

if __name__ == "__main__":
    test_api()
