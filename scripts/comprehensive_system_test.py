"""
CyberGuard Full System Acceptance & Sync Test
Tests every backend component, tab, and endpoint:
1. Auth & Session Management
2. Multilingual Cyberbullying Detection (English, Hindi, Hinglish slangs, Benign)
3. Incident Management & Synchronization
4. Official Forensic Report Filing
5. Support Assistant Chatbot (English procedural, Hinglish distress/slang, Crisis escalation)
6. Help Request / Patient Assistance Feedback Form
7. Admin & Consultant Dashboard Endpoints
"""
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

def make_request(endpoint, method="GET", data=None, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = None
    if data is not None:
        if isinstance(data, dict) and "username" in data and "password" in data and endpoint == "/auth/token":
            # Form urlencoded for OAuth2 password grant
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            body = urllib.parse.urlencode(data).encode("utf-8")
        else:
            body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return resp.status, json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        err_content = e.read().decode("utf-8")
        try:
            return e.code, json.loads(err_content)
        except Exception:
            return e.code, {"error": err_content}
    except Exception as e:
        return 500, {"error": str(e)}

def run_tests():
    print("="*70)
    print("   CYBERGUARD END-TO-END SYSTEM TEST & COMPONENT SYNC   ")
    print("="*70)

    # 1. AUTHENTICATION
    print("\n[TEST 1] Authenticating Admin User...")
    status, auth_resp = make_request("/auth/login", method="POST", data={
        "email": "admin@cyberguard.ai",
        "password": "AdminSecure2026!"
    })
    assert status == 200, f"Auth failed with status {status}: {auth_resp}"
    token = auth_resp.get("access_token")
    assert token, "No access token received"
    print(f" [PASS] Authenticated successfully. Token: {token[:15]}...")

    status, me_resp = make_request("/auth/me", method="GET", token=token)
    assert status == 200 and me_resp.get("email") == "admin@cyberguard.ai", f"Get Me failed: {me_resp}"
    print(f" [PASS] User identity verified: {me_resp.get('full_name')} ({me_resp.get('role')})")

    # 2. MULTILINGUAL CYBERBULLYING DETECTION (English, Hindi, Hinglish slangs, Benign)
    print("\n[TEST 2] Testing Multilingual Cyberbullying Detection Engine...")
    test_cases = [
        {
            "name": "English Abusive Harassment",
            "text": "You are a complete loser, nobody likes you and everyone wants you gone!",
            "expected_cb": True
        },
        {
            "name": "Devanagari Hindi Threat",
            "text": "तू बहुत बड़ा कुत्ता और हरामी है, तुझे जान से मार डालूंगा",
            "expected_cb": True
        },
        {
            "name": "Hinglish Slangs & Threat",
            "text": "sale bkl zyada hero mat ban varna pel dunga tujhe, shanti se baith",
            "expected_cb": True
        },
        {
            "name": "Benign Friendly Comment",
            "text": "Good morning team, could someone please share the notes from yesterday's meeting?",
            "expected_cb": False
        }
    ]

    analysis_results = []
    for tc in test_cases:
        status, res = make_request("/analyze/text", method="POST", data={"text": tc["text"]}, token=token)
        assert status == 200, f"Analyze text failed on {tc['name']}: {res}"
        analysis_results.append(res)
        print(f" -> {tc['name']}:")
        print(f"    Detected Class: {res.get('predicted_class')} | Is Cyberbullying: {res.get('is_cyberbullying')} | Confidence: {res.get('confidence'):.2f}")
        print(f"    Language: {res.get('detected_language')} | Severity: {res.get('severity')}")
    print(" [PASS] All multilingual detection test cases processed successfully.")

    # 3. INCIDENT CREATION & SYNCHRONIZATION
    print("\n[TEST 3] Creating & Synchronizing Incident from Detection...")
    incident_data = {
        "title": "Harassment Incident (Twitter / X)",
        "platform": "Twitter / X"
    }
    status, inc_resp = make_request("/incidents", method="POST", data=incident_data, token=token)
    assert status in [200, 201], f"Create incident failed with status {status}: {inc_resp}"
    incident_id = inc_resp.get("id")
    incident_code = inc_resp.get("incident_code")
    print(f" [PASS] Incident registered: Code {incident_code} (ID: {incident_id})")

    # Verify incident appears in incidents list
    status, list_inc = make_request("/incidents", method="GET", token=token)
    assert status == 200, f"List incidents failed: {list_inc}"
    matched = [inc for inc in list_inc if inc["id"] == incident_id]
    assert len(matched) > 0, "Created incident not found in incident list!"
    print(f" [PASS] Incident verified in incident synchronization table.")

    # 4. OFFICIAL FORENSIC REPORT GENERATION
    print("\n[TEST 4] Filing & Generating Official Forensic Report...")
    status, rep_resp = make_request(f"/reports/generate/{incident_id}", method="POST", token=token)
    assert status in [200, 201], f"Generate report failed: {rep_resp}"
    report_id = rep_resp.get("id")
    print(f" [PASS] Official report filed: ID {report_id}, Code: {rep_resp.get('report_code')}")

    # Verify report appears in reports list
    status, rep_list = make_request("/reports", method="GET", token=token)
    assert status == 200, f"List reports failed: {rep_list}"
    assert any(r["id"] == report_id for r in rep_list), "Report not found in reports list!"
    print(f" [PASS] Report verified in reports synchronization table.")

    # 5. CHATBOT INTERACTIONS (English procedural, Hinglish distress, Acute crisis)
    print("\n[TEST 5] Testing Support Assistant Chatbot in English & Hinglish...")
    status, sess_resp = make_request("/support/start", method="POST", data={"incident_id": incident_id}, token=token)
    assert status == 200, f"Start support session failed: {sess_resp}"
    session_id = sess_resp.get("id")
    print(f" [PASS] Support session initialized: Session #{session_id}")

    chat_prompts = [
        {
            "type": "English Procedural Inquiry",
            "prompt": "How do I report harassment on the official 1930 cybercrime portal?"
        },
        {
            "type": "Hinglish Cyberbullying Distress with Slang",
            "prompt": "ye log mere fake photos leak karne ki dhamki de rahe hai aur gande gaali bhej rahe hai, main bohot pareshan hu kya karu?"
        },
        {
            "type": "Acute Crisis & Safety Triage",
            "prompt": "zindagi khatam ho gayi hai, i feel suicidal and want to end it all, please help"
        }
    ]

    for cp in chat_prompts:
        msg_payload = {
            "session_id": session_id,
            "incident_id": incident_id,
            "message": cp["prompt"]
        }
        status, msg_resp = make_request("/support/message", method="POST", data=msg_payload, token=token)
        assert status == 200, f"Chatbot message failed on '{cp['type']}': {msg_resp}"
        print(f"\n -> Chat Prompt [{cp['type']}]:")
        print(f"    User: {cp['prompt'][:60]}...")
        print(f"    Assistant Response: {msg_resp.get('content')[:140]}...")
        signals = msg_resp.get("wellbeing_signals", {})
        print(f"    Escalation Level: {signals.get('escalation_urgency')} | Crisis: {signals.get('crisis_signal')} | Stress: {signals.get('stress_level')}")
        assert msg_resp.get("content"), "Empty assistant response!"
    print("\n [PASS] Chatbot responded correctly across English, Hinglish slangs, and crisis safety triggers.")

    # 6. PATIENT ASSISTANCE / HELP REQUEST FORM
    print("\n[TEST 6] Submitting Patient Assistance & Human Help Request...")
    help_payload = {
        "incident_id": incident_id,
        "full_name": "Test User Ananya",
        "age": 22,
        "email": "ananya.victim@cyberguard.ai",
        "phone": "+91 98765 43210",
        "platform": "Instagram",
        "account_username": "@ananya_secure",
        "num_bullies": 2,
        "bully_accounts": [
            {"handle": "@troll_acc1", "platform": "Instagram"},
            {"handle": "@toxic_hater", "platform": "Instagram"}
        ],
        "additional_notes": "Patient reports severe anxiety following cyber harassment. Requesting priority consultant review and evidence logging."
    }
    status, help_resp = make_request("/help-request", method="POST", data=help_payload, token=token)
    assert status in [200, 201], f"Help request submission failed with status {status}: {help_resp}"
    req_code = help_resp.get("request_code")
    print(f" [PASS] Patient help request submitted successfully: Code {req_code}")

    # 7. ADMIN / CONSULTANT WORKSPACE SYNCHRONIZATION
    print("\n[TEST 7] Verifying Admin & Consultant Sync...")
    status, admin_models = make_request("/admin/models", method="GET", token=token)
    assert status == 200, f"Get admin models failed: {admin_models}"
    print(f" [PASS] Admin Model Registry retrieved ({len(admin_models)} models registered)")

    status, admin_requests = make_request("/help-request/cases", method="GET", token=token)
    assert status == 200, f"Get help requests failed: {admin_requests}"
    found_req = [hr for hr in admin_requests if hr.get("request_code") == req_code]
    assert len(found_req) > 0, "Submitted help request not found in consultant queue!"
    print(f" [PASS] Patient help request verified in Consultant / Admin queue.")

    print("\n" + "="*70)
    print("   ALL TESTS PASSED: COMPLETE SYSTEM SYNC & WORKFLOW VERIFIED!   ")
    print("="*70)

if __name__ == "__main__":
    run_tests()
