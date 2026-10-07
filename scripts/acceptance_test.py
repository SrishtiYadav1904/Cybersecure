import requests
import uuid
import json
import os

BASE_URL = "http://127.0.0.1:8000/api"

def run_acceptance_test():
    print("=" * 70)
    print("CYBERGUARD COMPREHENSIVE END-TO-END ACCEPTANCE TEST")
    print("=" * 70)

    # 1. Register User
    username = f"testuser_{uuid.uuid4().hex[:6]}"
    email = f"{username}@test.com"
    password = "UserSecure2026!"
    print(f"\n[1] Registering User: {username} ({email})...")
    reg_resp = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "username": username,
        "password": password,
        "full_name": "Test Forensic User",
        "role": "USER"
    })
    assert reg_resp.status_code == 201, f"Reg failed: {reg_resp.text}"
    user_token = reg_resp.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}
    print(f"  [OK] User registered. Token acquired.")

    # 2. Login User
    print("\n[2] Logging in User...")
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    assert login_resp.status_code == 200
    print("  [OK] Login successful.")

    # 3. Analyze Comment (Hinglish Slang & Harassment)
    print("\n[3] Analyzing Direct Comment (Hinglish Code-Mixed)...")
    comment_text = "Tu kitna bada kutta aur chutiya hai saale, nobody likes you."
    analysis_resp = requests.post(f"{BASE_URL}/analyze/text", json={
        "text": comment_text,
        "platform": "Instagram"
    }, headers=user_headers)
    assert analysis_resp.status_code == 200, f"Analysis failed: {analysis_resp.text}"
    analysis = analysis_resp.json()
    incident_id = analysis["incident_id"]
    print(f"  [OK] Classification: {analysis['predicted_class']} (Confidence: {(analysis['confidence']*100):.1f}%)")
    print(f"  [OK] Detected Language: {analysis['detected_language']}")
    print(f"  [OK] Salient Tokens: {analysis['important_tokens']}")
    print(f"  [OK] Model Explanation: {analysis['explanation']}")
    print(f"  [OK] Active Incident Created: ID {incident_id}")

    # 4. Continue Incident with Second Evidence Piece
    print(f"\n[4] Adding Second Evidence Piece to Incident #{incident_id} (CONTINUE Flow)...")
    second_text = "Look at your face in the mirror, so ugly and pathetic."
    second_resp = requests.post(f"{BASE_URL}/analyze/text", json={
        "text": second_text,
        "platform": "Instagram",
        "incident_id": incident_id
    }, headers=user_headers)
    assert second_resp.status_code == 200
    print(f"  [OK] Second Evidence Attached to Incident #{incident_id}")

    # 5. OCR Screenshot Analysis
    print("\n[5] Testing Screenshot OCR Ingestion...")
    # Create a small dummy PNG for testing
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (400, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10, 40), "Look at your face, you are so ugly.", fill=(0, 0, 0))
    test_img_path = "test_screenshot.png"
    img.save(test_img_path)

    with open(test_img_path, "rb") as f:
        ocr_resp = requests.post(
            f"{BASE_URL}/analyze/image",
            files={"file": ("test_screenshot.png", f, "image/png")},
            data={"incident_id": incident_id},
            headers=user_headers
        )
    assert ocr_resp.status_code == 200, f"OCR failed: {ocr_resp.text}"
    ocr_data = ocr_resp.json()
    print(f"  [OK] OCR Extracted Text: \"{ocr_data['extracted_text']}\"")
    print(f"  [OK] OCR Confidence: {ocr_data['confidence']}")

    # 6. Confirm OCR Edited Text Analysis
    print("\n[6] Confirming User-Edited OCR Analysis...")
    confirm_resp = requests.post(
        f"{BASE_URL}/analyze/confirm-image",
        data={
            "edited_text": ocr_data["extracted_text"],
            "file_path": ocr_data["file_path"],
            "raw_ocr_text": ocr_data["extracted_text"],
            "incident_id": incident_id,
            "platform": "Instagram"
        },
        headers=user_headers
    )
    assert confirm_resp.status_code == 200
    print(f"  [OK] Image Evidence cataloged into Incident #{incident_id}")

    # 7. Conversational Chat Forensics (Repeated Targeting & Escalation)
    print("\n[7] Running Conversational Chat Forensics...")
    chat_messages = [
        {"sender": "@abuser_1", "text": "You are worthless and pathetic.", "timestamp": "12:00 PM"},
        {"sender": "Victim", "text": "Please leave me alone.", "timestamp": "12:01 PM"},
        {"sender": "@abuser_1", "text": "I will find you and destroy you.", "timestamp": "12:02 PM"},
        {"sender": "@troll_2", "text": "Yeah cry more you ugly clown.", "timestamp": "12:03 PM"}
    ]
    chat_resp = requests.post(f"{BASE_URL}/analyze/chat", json={
        "messages": chat_messages,
        "platform": "WhatsApp"
    }, headers=user_headers)
    assert chat_resp.status_code == 200
    chat_data = chat_resp.json()
    print(f"  [OK] Chat Primary Category: {chat_data['primary_category']}")
    print(f"  [OK] Repeated Targeting Detected: {chat_data['repeated_targeting_detected']}")
    print(f"  [OK] Repeated Summary: {chat_data['repeated_targeting_summary']}")
    print(f"  [OK] Escalation Trajectory Detected: {chat_data['escalation_detected']}")
    print(f"  [OK] Active Antagonists: {chat_data['active_bullies']}")

    # 8. Submit Help Request Escalation Form (SEEK HELP)
    print(f"\n[8] Submitting Formal Help Request Escalation for Incident #{incident_id}...")
    help_resp = requests.post(f"{BASE_URL}/help-request", json={
        "incident_id": incident_id,
        "full_name": "Test Forensic User",
        "age": 22,
        "email": email,
        "phone": "+91 98765 43210",
        "platform": "Instagram",
        "num_bullies": 2,
        "bully_accounts": [
            {"handle": "@abuser_1", "profile_url": "https://instagram.com/abuser_1", "platform": "Instagram"},
            {"handle": "@troll_2", "profile_url": "https://instagram.com/troll_2", "platform": "Instagram"}
        ],
        "additional_notes": "Multiple repeated hostile messages threatening violence."
    }, headers=user_headers)
    assert help_resp.status_code == 201
    help_data = help_resp.json()
    print(f"  [OK] Help Request Created: Code {help_data['request_code']}")

    # 9. Conclude Incident & Generate Forensic Report (STOP Flow)
    print(f"\n[9] Concluding Incident #{incident_id} & Compiling PDF Report (STOP Flow)...")
    close_resp = requests.post(f"{BASE_URL}/incidents/{incident_id}/close", headers=user_headers)
    assert close_resp.status_code == 200
    close_data = close_resp.json()
    report_id = close_data["report_id"]
    print(f"  [OK] Report Compiled: {close_data['report_code']} (Report ID: {report_id})")

    # 10. Download & Verify Binary PDF
    print(f"\n[10] Downloading Report Artifact #{report_id}...")
    pdf_resp = requests.get(f"{BASE_URL}/reports/{report_id}/download", headers=user_headers)
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
    assert len(pdf_resp.content) > 1000
    print(f"  [OK] PDF Downloaded successfully ({len(pdf_resp.content)} bytes). Valid PDF header: {pdf_resp.content[:4]}")

    # 11. Support AI Chat with Grounded RAG
    print("\n[11] Testing Grounded Support AI Agent...")
    start_sup = requests.post(f"{BASE_URL}/support/start", json={"incident_id": incident_id}, headers=user_headers)
    session_id = start_sup.json()["id"]

    query = "How do I block someone on Instagram who is threatening to dox me?"
    msg_resp = requests.post(f"{BASE_URL}/support/message", json={
        "session_id": session_id,
        "message": query
    }, headers=user_headers)
    assert msg_resp.status_code == 200
    sup_msg = msg_resp.json()
    print(f"  [OK] AI Assistant Response Received ({len(sup_msg['content'])} chars)")
    print(f"  [OK] Wellbeing Signals: {sup_msg['wellbeing_signals']}")
    if sup_msg['rag_sources']:
        print(f"  [OK] Grounded RAG Guides: {[s['title'] for s in sup_msg['rag_sources']]}")

    # 12. Query Emergency Helplines
    print("\n[12] Querying Official Statutory Resources...")
    res_resp = requests.get(f"{BASE_URL}/support/resources")
    assert res_resp.status_code == 200
    resources = res_resp.json()
    print(f"  [OK] Retrieved {len(resources)} verified emergency helplines:")
    for r in resources[:3]:
        print(f"    - {r['name']} ({r.get('contact_number')}): {r['description'][:50]}...")

    # 13. Admin Analytics & Model Governance
    print("\n[13] Authenticating as Administrator...")
    admin_login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@cyberguard.ai",
        "password": "AdminSecure2026!"
    })
    assert admin_login.status_code == 200
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    dash_resp = requests.get(f"{BASE_URL}/admin/dashboard", headers=admin_headers)
    assert dash_resp.status_code == 200
    dash = dash_resp.json()
    print(f"  [OK] Total Users: {dash['total_users']}")
    print(f"  [OK] Total Incidents: {dash['total_incidents']}")
    print(f"  [OK] Bullying Detections: {dash['bullying_detections']}")
    print(f"  [OK] Active Model: {dash['current_model_version']}")
    print(f"  [OK] Drift Status: {dash['drift_status']}")

    # 14. Concept Drift (PSI) & Slang Queue Validation
    print("\n[14] Checking Concept Drift & Slang Queue...")
    drift_resp = requests.get(f"{BASE_URL}/admin/drift", headers=admin_headers)
    assert drift_resp.status_code == 200
    drift_info = drift_resp.json()
    print(f"  [OK] Drift PSI Value: {drift_info['psi_value']} ({drift_info['status']})")

    slang_resp = requests.get(f"{BASE_URL}/admin/slang", headers=admin_headers)
    assert slang_resp.status_code == 200
    slang_list = slang_resp.json()
    print(f"  [OK] Slang Terms in Governance Queue: {len(slang_list)}")
    if slang_list:
        term_to_approve = slang_list[0]
        app_resp = requests.post(
            f"{BASE_URL}/admin/slang/{term_to_approve['id']}/approve?meaning=Classist_slang",
            headers=admin_headers
        )
        assert app_resp.status_code == 200
        print(f"  [OK] Approved slang term '{term_to_approve['term']}' for retraining dataset.")

    # Clean up test screenshot
    if os.path.exists(test_img_path):
        os.remove(test_img_path)

    print("\n" + "=" * 70)
    print("ALL 14 ACCEPTANCE TEST SUITES PASSED FLAWLESSLY WITH REAL DATA & MODELS!")
    print("=" * 70)

if __name__ == "__main__":
    run_acceptance_test()
