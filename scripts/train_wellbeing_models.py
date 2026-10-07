"""
CyberGuard Wellbeing Support Model Training Pipeline (SUP-001)
Pure Machine Learning Pipeline: Zero hardcoded keyword if/else fallbacks.
Trains 4 ML model heads directly on semantic embeddings:
1. Crisis Triage (CatBoost): CRISIS_ESCALATION vs DEPRESSIVE_DISTRESS vs STANDARD_WELLBEING
2. Cognitive Distress (LightGBM): LOSS_OF_SELF_DETECTED vs NORMAL_AFFECT
3. Stress Severity (Calibrated Classifier): LOW vs MODERATE vs HIGH vs SEVERE
4. Chatbot Action Policy (Contextual Classifier):
   safety_crisis_intervention_and_helpline vs empathetic_validation_and_active_listening vs cognitive_reframing_and_self_compassion vs supportive_open_dialogue
"""
import os
import sys
import time
import json
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import lightgbm as lgb
import catboost as cb
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ml.feature_engineering.context_encoder import ContextualEncoder
from ml.preprocessing.normalizer import normalize_text

SAVE_DIR = PROJECT_ROOT / "trained_models" / "support" / "SUP-001"
FALLBACK_SAVE_DIR = PROJECT_ROOT / "trained_models" / "support_model"
EVAL_DIR = PROJECT_ROOT / "artifacts" / "evaluation"
DATA_DIR = PROJECT_ROOT / "data" / "unified" / "wellbeing"

for d in [SAVE_DIR, FALLBACK_SAVE_DIR, EVAL_DIR, DATA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def compute_hash(text):
    return hashlib.sha256(str(text).encode('utf-8')).hexdigest()

def build_wellbeing_dataset():
    records = []
    seen_hashes = set()

    # 1. Procedural, informational, and normal wellbeing prompts (for STANDARD_WELLBEING & LOW stress)
    procedural_samples = [
        "How do I report online harassment on the 1930 portal?",
        "Can you guide me on how to file a formal cybercrime report in India?",
        "What are the steps to report an abusive account on Instagram?",
        "How can I block someone on social media without losing evidence?",
        "How do I take screenshots that are valid in court or for police complaints?",
        "Where is the National Cyber Crime Reporting Portal located?",
        "What is the toll-free number for cyber fraud and cyber harassment?",
        "How do I change my account privacy settings so strangers cannot message me?",
        "Can you explain how two-factor authentication works?",
        "What should I do if someone creates a fake profile using my photos?",
        "Can you give me tips on maintaining digital safety and privacy?",
        "What evidence is required when filing a police FIR for online bullying?",
        "How do I report WhatsApp group harassment?",
        "Can someone be arrested for cyberbullying in India under the IT Act?",
        "What is Section 66E and 67 of the Information Technology Act?",
        "How do I report non-consensual image sharing?",
        "Can I report anonymously on cybercrime.gov.in?",
        "How do I keep my phone safe from spyware or unauthorized access?",
        "Hello, I need some safety guidance on social media settings.",
        "Good morning, can you explain how this support portal helps victims?",
        "What features does CyberGuard offer for incident management?",
        "How do I export my incident report to a PDF document?",
        "How to block calls and messages from unknown numbers on WhatsApp?",
        "What is the difference between blocking and restricting an account?",
        "How do I report defamation on YouTube comments?",
        "Who can I contact if someone is trolling my business page?",
        "Can you give me the helpline numbers for women safety and child cyber safety?",
        "How do I preserve metadata of an abusive email or chat?",
        "What should I do if an abuser deletes their message after sending it?",
        "How does the evidence preservation workflow work?",
        "1930 portal par cybercrime report kaise kare?",
        "Police complaint karne ke liye kya evidence chahiye?",
        "Instagram account par privacy settings kaise lagaye?",
        "WhatsApp group me harassment ho raha hai to kaise report kare?",
        "Cyber crime portal par complaint darj karne ke steps kya hai?",
        "Online security aur safety ke baare me jankari chahiye.",
        "Mere account ko safe rakhne ke liye kya tips hai?"
    ]

    for p_text in procedural_samples:
        nt = normalize_text(p_text)
        thash = compute_hash(nt)
        seen_hashes.add(thash)
        # Task A: Crisis Triage -> STANDARD_WELLBEING
        records.append({
            "text": p_text,
            "normalized_text": nt,
            "label": "STANDARD_WELLBEING",
            "task": "CRISIS_TRIAGE",
            "source_dataset": "procedural_safety_prompts",
            "source_label": "procedural",
            "language": "English",
            "text_hash": f"{thash}_triage",
            "action_policy": "supportive_open_dialogue"
        })
        # Task B: Cognitive Distress -> NORMAL_AFFECT
        records.append({
            "text": p_text,
            "normalized_text": nt,
            "label": "NORMAL_AFFECT",
            "task": "COGNITIVE_DISTRESS",
            "source_dataset": "procedural_safety_prompts",
            "source_label": "normal",
            "language": "English",
            "text_hash": f"{thash}_lost",
            "action_policy": "supportive_open_dialogue"
        })
        # Task C: Stress Severity -> LOW
        records.append({
            "text": p_text,
            "normalized_text": nt,
            "label": "LOW",
            "task": "STRESS_CALIBRATION",
            "source_dataset": "procedural_safety_prompts",
            "source_label": "low",
            "language": "English",
            "text_hash": f"{thash}_stress",
            "action_policy": "supportive_open_dialogue"
        })

    # Repeat procedural samples to ensure balanced representation against crisis/depression
    procedural_records = list(records)
    for _ in range(8):
        records.extend(procedural_records)

    # 2. Ingest Processed Mental Health Combined Dataset
    proc_mh_path = PROJECT_ROOT / "processed" / "mental_health_combined.csv"
    if proc_mh_path.exists():
        print(f"Loading processed mental health dataset: {proc_mh_path}")
        df_mh = pd.read_csv(proc_mh_path)
        print(f"Processed mental health records: {len(df_mh)}")

        for _, row in df_mh.iterrows():
            raw_text = str(row.get("text_raw", ""))
            clean_text = str(row.get("text_cleaned", ""))
            if not clean_text or clean_text == "nan":
                clean_text = normalize_text(raw_text)
            if len(clean_text) < 10:
                continue

            thash = compute_hash(clean_text)
            if thash in seen_hashes:
                continue
            seen_hashes.add(thash)

            # Map Crisis Triage task
            is_crisis = int(row.get("is_crisis", 0))
            mental_state = str(row.get("mental_state", ""))
            if is_crisis == 1 or mental_state == "suicide_crisis":
                crisis_lbl = "CRISIS_ESCALATION"
            elif mental_state == "normal_supportive":
                crisis_lbl = "STANDARD_WELLBEING"
            else:
                crisis_lbl = "DEPRESSIVE_DISTRESS"

            records.append({
                "text": raw_text[:1200],
                "normalized_text": clean_text[:1200],
                "label": crisis_lbl,
                "task": "CRISIS_TRIAGE",
                "source_dataset": f"processed_{row.get('source', 'mental_health')}",
                "source_label": mental_state,
                "language": "English",
                "text_hash": f"{thash}_crisis",
                "action_policy": str(row.get("recommended_chatbot_action", "empathetic_validation_and_active_listening"))
            })

            # Map Cognitive Distress task
            loss_of_self = int(row.get("loss_of_self", 0))
            lost_lbl = "LOSS_OF_SELF_DETECTED" if loss_of_self == 1 else "NORMAL_AFFECT"
            records.append({
                "text": raw_text[:1200],
                "normalized_text": clean_text[:1200],
                "label": lost_lbl,
                "task": "COGNITIVE_DISTRESS",
                "source_dataset": f"processed_{row.get('source', 'mental_health')}",
                "source_label": str(loss_of_self),
                "language": "English",
                "text_hash": f"{thash}_lost",
                "action_policy": str(row.get("recommended_chatbot_action", "empathetic_validation_and_active_listening"))
            })

            # Map Stress Severity calibration
            stress_lbl = "SEVERE" if is_crisis == 1 else ("HIGH" if loss_of_self == 1 else "MODERATE")
            records.append({
                "text": raw_text[:1200],
                "normalized_text": clean_text[:1200],
                "label": stress_lbl,
                "task": "STRESS_CALIBRATION",
                "source_dataset": f"processed_{row.get('source', 'mental_health')}",
                "source_label": stress_lbl,
                "language": "English",
                "text_hash": f"{thash}_stress",
                "action_policy": str(row.get("recommended_chatbot_action", "empathetic_validation_and_active_listening"))
            })

    # 3. Add synthetic support wellbeing dataset
    synth_path = PROJECT_ROOT / "data" / "raw" / "support_wellbeing_raw.csv"
    if synth_path.exists():
        df_sw = pd.read_csv(synth_path)
        for _, row in df_sw.iterrows():
            rt = str(row.get("text", ""))
            nt = normalize_text(rt)
            thash = compute_hash(nt)
            if thash not in seen_hashes:
                seen_hashes.add(thash)
                sl = str(row.get("stress_label", "MODERATE")).upper()
                c_lbl = "STANDARD_WELLBEING" if sl == "LOW" else "DEPRESSIVE_DISTRESS"
                records.append({
                    "text": rt,
                    "normalized_text": nt,
                    "label": c_lbl,
                    "task": "CRISIS_TRIAGE",
                    "source_dataset": "Synthetic-Support-v1",
                    "source_label": sl,
                    "language": "English",
                    "text_hash": f"{thash}_synth_c",
                    "action_policy": "supportive_open_dialogue"
                })
                records.append({
                    "text": rt,
                    "normalized_text": nt,
                    "label": sl,
                    "task": "STRESS_CALIBRATION",
                    "source_dataset": "Synthetic-Support-v1",
                    "source_label": sl,
                    "language": "English",
                    "text_hash": f"{thash}_synth_s",
                    "action_policy": "supportive_open_dialogue"
                })

    df_all = pd.DataFrame(records)
    return df_all

def train_wellbeing_models():
    print("\n=======================================================")
    print("   TRAINING PURE ML WELLBEING SUPPORT INTELLIGENCE     ")
    print("=======================================================")

    df_all = build_wellbeing_dataset()
    print(f"\nUnified Wellbeing & Chatbot Dataset: {len(df_all)} total task records")
    print(df_all["task"].value_counts())

    encoder = ContextualEncoder(output_dim=384)
    print("Extracting contextual embeddings (384d)...")

    # ---------------------------------------------------------
    # 1. TASK A: CRISIS TRIAGE (CatBoost with 3 Classes)
    # ---------------------------------------------------------
    print("\n--- 1. Training Task A: Crisis Triage Model (Pure ML) ---")
    df_crisis = df_all[df_all["task"] == "CRISIS_TRIAGE"].reset_index(drop=True)
    print("Crisis Triage Class Distribution:\n", df_crisis["label"].value_counts())

    train_c, test_c = train_test_split(df_crisis, test_size=0.2, random_state=42, stratify=df_crisis["label"])

    X_train_c = encoder.encode_batch(train_c["normalized_text"].tolist())
    X_test_c = encoder.encode_batch(test_c["normalized_text"].tolist())

    crisis_le = LabelEncoder()
    y_train_c_enc = crisis_le.fit_transform(train_c["label"].tolist())
    y_test_c_enc = crisis_le.transform(test_c["label"].tolist())

    cb_crisis = cb.CatBoostClassifier(iterations=80, depth=5, learning_rate=0.1, random_seed=42, thread_count=4, verbose=0)
    cb_crisis.fit(X_train_c, y_train_c_enc)

    preds_c_enc = cb_crisis.predict(X_test_c)
    preds_c = crisis_le.inverse_transform(preds_c_enc)

    acc_c = accuracy_score(test_c["label"].tolist(), preds_c)
    f1_c = f1_score(test_c["label"].tolist(), preds_c, average="macro", zero_division=0)
    print(f"Crisis Triage Test Accuracy: {acc_c:.4f}, Macro-F1: {f1_c:.4f}")
    print(f"Classes: {list(crisis_le.classes_)}")

    joblib.dump(cb_crisis, SAVE_DIR / "crisis_triage_model.joblib")
    joblib.dump(crisis_le, SAVE_DIR / "crisis_label_encoder.joblib")

    # ---------------------------------------------------------
    # 2. TASK B: COGNITIVE DISTRESS / LoST (LightGBM)
    # ---------------------------------------------------------
    print("\n--- 2. Training Task B: Cognitive Distress / LoST Model ---")
    df_lost = df_all[df_all["task"] == "COGNITIVE_DISTRESS"].reset_index(drop=True)
    train_l, test_l = train_test_split(df_lost, test_size=0.2, random_state=42, stratify=df_lost["label"])

    X_train_l = encoder.encode_batch(train_l["normalized_text"].tolist())
    X_test_l = encoder.encode_batch(test_l["normalized_text"].tolist())

    lost_le = LabelEncoder()
    y_train_l_enc = lost_le.fit_transform(train_l["label"].tolist())
    y_test_l_enc = lost_le.transform(test_l["label"].tolist())

    lgb_lost = lgb.LGBMClassifier(n_estimators=80, max_depth=5, learning_rate=0.1, random_state=42, n_jobs=4, verbose=-1)
    lgb_lost.fit(X_train_l, y_train_l_enc)

    preds_l_enc = lgb_lost.predict(X_test_l)
    preds_l = lost_le.inverse_transform(preds_l_enc)
    acc_l = accuracy_score(test_l["label"].tolist(), preds_l)
    f1_l = f1_score(test_l["label"].tolist(), preds_l, average="macro", zero_division=0)
    print(f"Cognitive Distress Test Accuracy: {acc_l:.4f}, Macro-F1: {f1_l:.4f}")

    joblib.dump(lgb_lost, SAVE_DIR / "cognitive_distortion_model.joblib")
    joblib.dump(lost_le, SAVE_DIR / "lost_label_encoder.joblib")

    # ---------------------------------------------------------
    # 3. TASK C: STRESS SEVERITY CALIBRATOR
    # ---------------------------------------------------------
    print("\n--- 3. Training Task C: Stress Severity Calibrator ---")
    df_stress = df_all[df_all["task"] == "STRESS_CALIBRATION"].reset_index(drop=True)
    stress_classes = ["LOW", "MODERATE", "HIGH", "SEVERE"]
    stress_le = LabelEncoder()
    stress_le.fit(stress_classes)

    clean_stress_labels = [
        s if s in stress_classes else "MODERATE"
        for s in df_stress["label"].tolist()
    ]
    df_stress["clean_label"] = clean_stress_labels

    train_s, test_s = train_test_split(df_stress, test_size=0.2, random_state=42, stratify=df_stress["clean_label"])

    X_train_s = encoder.encode_batch(train_s["normalized_text"].tolist())
    X_test_s = encoder.encode_batch(test_s["normalized_text"].tolist())

    stress_model = LogisticRegression(max_iter=500, random_state=42)
    stress_model.fit(X_train_s, stress_le.transform(train_s["clean_label"].tolist()))

    preds_s_enc = stress_model.predict(X_test_s)
    preds_s = stress_le.inverse_transform(preds_s_enc)
    acc_s = accuracy_score(test_s["clean_label"].tolist(), preds_s)
    f1_s = f1_score(test_s["clean_label"].tolist(), preds_s, average="macro", zero_division=0)
    print(f"Stress Calibrator Accuracy: {acc_s:.4f}, Macro-F1: {f1_s:.4f}")

    joblib.dump(stress_model, SAVE_DIR / "stress_level_model.joblib")
    joblib.dump(stress_le, SAVE_DIR / "stress_label_encoder.joblib")

    # Fallback directory
    joblib.dump(stress_model, FALLBACK_SAVE_DIR / "stress_classifier.joblib")

    # ---------------------------------------------------------
    # 4. TASK D: CHATBOT ACTION POLICY CLASSIFIER
    # ---------------------------------------------------------
    print("\n--- 4. Training Task D: Chatbot Action Policy Classifier ---")
    df_action = df_all[df_all["action_policy"].notna()].copy()
    action_le = LabelEncoder()
    action_y = action_le.fit_transform(df_action["action_policy"].tolist())
    action_texts = df_action["normalized_text"].tolist()

    train_act_idx, test_act_idx = train_test_split(
        np.arange(len(action_y)), test_size=0.2, random_state=42, stratify=action_y
    )
    X_train_act = encoder.encode_batch([action_texts[i] for i in train_act_idx])
    X_test_act = encoder.encode_batch([action_texts[i] for i in test_act_idx])

    action_clf = LogisticRegression(max_iter=500, random_state=42)
    action_clf.fit(X_train_act, action_y[train_act_idx])

    preds_act = action_clf.predict(X_test_act)
    acc_act = accuracy_score(action_y[test_act_idx], preds_act)
    f1_act = f1_score(action_y[test_act_idx], preds_act, average="macro", zero_division=0)
    print(f"Chatbot Action Policy Test Accuracy: {acc_act:.4f}, Macro-F1: {f1_act:.4f}")

    joblib.dump(action_clf, SAVE_DIR / "chatbot_action_model.joblib")
    joblib.dump(action_le, SAVE_DIR / "action_label_encoder.joblib")

    # Save manifest
    all_metrics = [
        {"task": "CRISIS_TRIAGE", "model_name": "CatBoost (384d)", "accuracy": round(float(acc_c), 4), "macro_f1": round(float(f1_c), 4), "classes": list(crisis_le.classes_)},
        {"task": "COGNITIVE_DISTRESS", "model_name": "LightGBM (384d)", "accuracy": round(float(acc_l), 4), "macro_f1": round(float(f1_l), 4), "classes": list(lost_le.classes_)},
        {"task": "STRESS_SEVERITY", "model_name": "Logistic Regression (384d)", "accuracy": round(float(acc_s), 4), "macro_f1": round(float(f1_s), 4), "classes": stress_classes},
        {"task": "ACTION_POLICY", "model_name": "Contextual Policy Classifier", "accuracy": round(float(acc_act), 4), "macro_f1": round(float(f1_act), 4), "classes": list(action_le.classes_)}
    ]

    manifest = {
        "model_version": "SUP-001",
        "dataset_version": "WB-PURE-ML-003",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tasks": all_metrics
    }
    with open(SAVE_DIR / "training_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nAll Wellbeing Support Models successfully saved to {SAVE_DIR}/")

if __name__ == "__main__":
    train_wellbeing_models()
