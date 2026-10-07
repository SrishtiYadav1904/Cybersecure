import os
import json
import re
from typing import Dict, List, Any, Tuple
from pathlib import Path
import numpy as np
import joblib

from backend.app.config import settings
from ml.feature_engineering.context_encoder import ContextualEncoder

class SupportAIAgent:
    """
    Ground-truth anchored Support Assistant with RAG & SUP-001 Machine Learning:
    - Trained ML Model Family (SUP-001):
        * CatBoost Crisis Triage Classifier (WB-DATA-001)
        * LightGBM LoST Cognitive Distress Classifier (WB-DATA-001)
        * Calibrated Stress Level Calibrator (WB-DATA-001)
    - Queries official guides (blocking, privacy, cybercrime portal 1930, Tele-MANAS 14416)
    - Strictly avoids clinical mental health diagnosis (ethical non-diagnostic boundary)
    - Recommends consultant escalation and emergency resources when risk is elevated
    """

    def __init__(self, kb_dir: str = None, model_dir: str = None):
        self.kb_dir = kb_dir or settings.KNOWLEDGE_BASE_DIR
        self.model_dir = model_dir or os.path.join(os.path.dirname(__file__), "..", "..", "..", "trained_models", "support", "SUP-001")
        self.documents = []
        self.resources = []
        self.context_encoder = ContextualEncoder(output_dim=384)
        
        # Load trained ML models
        self.crisis_model = None
        self.crisis_le = None
        self.cognitive_model = None
        self.lost_le = None
        self.stress_model = None
        self.stress_le = None
        self.action_model = None
        self.action_le = None
        
        self._load_support_models()
        self._load_knowledge_base()

    def _load_support_models(self):
        """Loads trained SUP-001 wellbeing and triage classifiers."""
        if not os.path.exists(self.model_dir):
            return
        try:
            c_path = os.path.join(self.model_dir, "crisis_triage_model.joblib")
            cle_path = os.path.join(self.model_dir, "crisis_label_encoder.joblib")
            if os.path.exists(c_path) and os.path.exists(cle_path):
                self.crisis_model = joblib.load(c_path)
                self.crisis_le = joblib.load(cle_path)

            cog_path = os.path.join(self.model_dir, "cognitive_distortion_model.joblib")
            lostle_path = os.path.join(self.model_dir, "lost_label_encoder.joblib")
            if os.path.exists(cog_path) and os.path.exists(lostle_path):
                self.cognitive_model = joblib.load(cog_path)
                self.lost_le = joblib.load(lostle_path)

            s_path = os.path.join(self.model_dir, "stress_level_model.joblib")
            sle_path = os.path.join(self.model_dir, "stress_label_encoder.joblib")
            if os.path.exists(s_path) and os.path.exists(sle_path):
                self.stress_model = joblib.load(s_path)
                self.stress_le = joblib.load(sle_path)

            act_path = os.path.join(self.model_dir, "chatbot_action_model.joblib")
            actle_path = os.path.join(self.model_dir, "action_label_encoder.joblib")
            if os.path.exists(act_path) and os.path.exists(actle_path):
                self.action_model = joblib.load(act_path)
                self.action_le = joblib.load(actle_path)
        except Exception as e:
            print(f"Warning loading SUP-001 models: {e}")

    def _load_knowledge_base(self):
        """Index all markdown guides and official resources.json."""
        if not os.path.exists(self.kb_dir):
            return

        for root, _, files in os.walk(self.kb_dir):
            for f in files:
                filepath = os.path.join(root, f)
                if f.endswith(".md"):
                    with open(filepath, "r", encoding="utf-8") as file:
                        content = file.read()
                        rel_path = os.path.relpath(filepath, self.kb_dir)
                        self.documents.append({
                            "title": f.replace(".md", "").replace("_", " ").title(),
                            "path": rel_path,
                            "content": content,
                            "type": "guide"
                        })
                elif f in ["resources.json", "helplines.json"]:
                    try:
                        with open(filepath, "r", encoding="utf-8") as file:
                            res_list = json.load(file)
                            for res in res_list:
                                self.resources.append(res)
                                name = res.get("resource_name") or res.get("name", "Helpline")
                                phone = res.get("phone") or res.get("contact_number", "")
                                desc = res.get("description", "")
                                url = res.get("url") or res.get("website", "")
                                self.documents.append({
                                    "title": name,
                                    "path": f"resources/{f}",
                                    "content": f"{name} ({phone}): {desc} {url}",
                                    "type": "resource",
                                    "data": res
                                })
                    except Exception:
                        pass

    def retrieve_rag_context(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Keyword & semantic retrieval over indexed knowledge base documents."""
        query_words = set(re.findall(r'\w+', query.lower()))
        scored_docs = []

        for doc in self.documents:
            content_lower = doc["content"].lower()
            title_lower = doc["title"].lower()

            score = 0
            for w in query_words:
                if len(w) <= 2:
                    continue
                if w in title_lower:
                    score += 5
                if w in content_lower:
                    score += 1

            if score > 0:
                scored_docs.append((score, doc))

            scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:top_k]]

    def assess_wellbeing_indicators(self, text: str) -> Dict[str, Any]:
        """
        Evaluate non-diagnostic emotional and stress indicators using SUP-001 ML models:
        - Crisis Triage Signal: CRISIS_ESCALATION, DEPRESSIVE_DISTRESS, STANDARD_WELLBEING
        - Stress Level: LOW, MODERATE, HIGH, SEVERE
        - Cognitive Distress: LOSS_OF_SELF_DETECTED, NORMAL_AFFECT
        - Escalation Urgency: NORMAL, ADVISORY, URGENT_ESCALATION
        - Action Policy: recommended chatbot behavior policy
        """
        lower = text.lower()

        # Multilingual crisis cues (English + Hindi / Hinglish + modern slangs)
        crisis_signals = [
            "kill myself", "end my life", "suicide", "suicidal", "want to die", "hurt myself", 
            "can't live", "give up on life", "end it all", "kms", "mar jana chahta", "mar jau", 
            "jaan de dunga", "zindagi khatam", "jeena nahi chahta", "marne ka mann", "sab khatam ho gaya"
        ]
        has_crisis_keyword = any(sig in lower for sig in crisis_signals)

        # Procedural / operational query detection (English + Hindi / Hinglish)
        procedural_keywords = [
            "how do i", "how to", "how can i", "block", "reporting", "guide", "steps", 
            "procedure", "settings", "portal", "police", "what should i do", "kaise kare", 
            "kya karu", "report kaise", "complaint kaise", "1930", "fir kaise", "help kaise"
        ]
        is_procedural = any(kw in lower for kw in procedural_keywords)

        # Distress keywords (English + Hindi / Hinglish)
        distress_keywords = [
            "sad", "depressed", "hopeless", "crying", "broken", "hurts", "pain", "unbearable", 
            "worthless", "alone", "scared", "terrified", "panic", "pareshan", "rona aa raha", 
            "tut gaya", "dar lag raha", "khauf", "tension", "dimag kharab", "ghabrahat", "harass"
        ]
        has_distress_keyword = any(dkw in lower for dkw in distress_keywords)

        # ML-based Evaluation
        emb = self.context_encoder.encode(text).reshape(1, -1)

        # 1. Crisis Triage
        crisis_signal = "STANDARD_WELLBEING"
        if has_crisis_keyword:
            crisis_signal = "CRISIS_ESCALATION"
        elif has_distress_keyword and self.crisis_model and self.crisis_le:
            try:
                probs = self.crisis_model.predict_proba(emb)[0]
                classes = list(self.crisis_le.classes_)
                if "CRISIS_ESCALATION" in classes:
                    esc_idx = classes.index("CRISIS_ESCALATION")
                    if probs[esc_idx] >= 0.65:
                        crisis_signal = "CRISIS_ESCALATION"
                    else:
                        crisis_signal = "DEPRESSIVE_DISTRESS"
                else:
                    crisis_signal = "DEPRESSIVE_DISTRESS"
            except Exception:
                crisis_signal = "DEPRESSIVE_DISTRESS"
        elif is_procedural:
            crisis_signal = "STANDARD_WELLBEING"

        # 2. Cognitive Distress
        cognitive_distress = "NORMAL_AFFECT"
        if has_distress_keyword and self.cognitive_model and self.lost_le:
            try:
                cog_pred_idx = self.cognitive_model.predict(emb)
                cognitive_distress = self.lost_le.inverse_transform(cog_pred_idx)[0]
            except Exception:
                pass

        # 3. Stress Level
        if is_procedural and not has_distress_keyword and not has_crisis_keyword:
            stress_level = "LOW"
        else:
            stress_level = "MODERATE"
            if self.stress_model and self.stress_le:
                try:
                    s_pred_idx = self.stress_model.predict(emb)
                    stress_level = self.stress_le.inverse_transform(s_pred_idx)[0]
                except Exception:
                    pass

        # 4. Action Policy
        action_policy = "empathetic_validation_and_active_listening"
        if self.action_model and self.action_le:
            try:
                act_pred_idx = self.action_model.predict(emb)
                action_policy = self.action_le.inverse_transform(act_pred_idx)[0]
            except Exception:
                pass

        # Determine escalation urgency
        if crisis_signal == "CRISIS_ESCALATION":
            escalation = "URGENT_ESCALATION"
            stress_level = "SEVERE"
            action_policy = "safety_crisis_intervention_and_helpline"
        elif stress_level in ["HIGH", "SEVERE"] or cognitive_distress == "LOSS_OF_SELF_DETECTED":
            escalation = "ADVISORY"
        else:
            escalation = "NORMAL"

        return {
            "model_family": "support_model",
            "model_version": "SUP-001",
            "dataset_version": "WB-DATA-COMBINED-002",
            "crisis_signal": crisis_signal,
            "stress_level": stress_level,
            "cognitive_distress": cognitive_distress,
            "action_policy": action_policy,
            "escalation_urgency": escalation,
            "requires_hotline_modal": (crisis_signal == "CRISIS_ESCALATION"),
            "ethical_notice": "Non-diagnostic wellbeing signal. Not a medical or psychiatric diagnosis."
        }

    def _is_hindi_or_hinglish(self, text: str) -> bool:
        """Heuristic detection of Hindi (Devanagari) or Hinglish slang."""
        if re.search(r'[\u0900-\u097F]', text):
            return True
        hinglish_words = {
            "kya", "kyu", "hai", "nahi", "bhai", "tere", "mera", "meri", "karo", "tu", "teri",
            "sale", "kamina", "pagal", "bkl", "mc", "bc", "chutiya", "gandu", "moti", "bhaisn",
            "marr", "jaa", "kutta", "kamine", "harami", "dost", "yaar", "aur", "hota", "hoga",
            "karu", "raha", "rahi", "bolo", "madad", "dar", "dhamki", "khatam", "pareshan"
        }
        tokens = set(re.findall(r'\b[a-zA-Z]+\b', text.lower()))
        return len(tokens.intersection(hinglish_words)) >= 1

    def generate_response(
        self,
        user_message: str,
        incident_context: Dict[str, Any] = None,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Generates empathetic, factually grounded response with safety guardrails across English, Hindi, and Hinglish.
        """
        indicators = self.assess_wellbeing_indicators(user_message)
        rag_docs = self.retrieve_rag_context(user_message, top_k=2)
        sources_used = [doc["title"] for doc in rag_docs]
        is_hindi = self._is_hindi_or_hinglish(user_message)

        # 1. Acute crisis safety layer
        if indicators["requires_hotline_modal"]:
            if is_hindi:
                response_text = (
                    "Main samajh sakta hu ki aap is waqt kitne dard aur stress mein hain. Par please vishwas kijiye, "
                    "aap bilkul akele nahi hain aur aapki jaan bohot keemti hai. "
                    "Aapki madad ke liye trained counselors 24x7 uplabdh hain:\n\n"
                    "• **Tele-MANAS (Govt. of India):** Call **14416** (24x7 Toll-Free)\n"
                    "• **National Cyber Crime Helpline:** Call **1930** (24x7)\n"
                    "• **Vandrevala Foundation Helpline:** Call **+91 9999 666 555**\n"
                    "• **KIRAN Helpline:** Call **1800-599-0019**\n\n"
                    "Please bina kisi jhijhak ke in numbers par turant call karein ya kisi bharosemand insan se baat karein."
                )
            else:
                response_text = (
                    "I hear how much pain you are going through right now, but please know that you do not have to carry this alone. "
                    "There are trained professionals available right now who want to support you:\n\n"
                    "• **Tele-MANAS (Government of India):** Call **14416** (24x7 Toll-Free)\n"
                    "• **National Cyber Crime Helpline:** Call **1930** (24x7)\n"
                    "• **Vandrevala Foundation Helpline:** Call **+91 9999 666 555**\n"
                    "• **KIRAN Helpline:** Call **1800-599-0019**\n\n"
                    "Please reach out to one of these numbers immediately or talk to someone you trust."
                )
            return {
                "response": response_text,
                "rag_sources": ["Tele-MANAS (14416)", "National Cyber Crime Helpline (1930)"],
                "wellbeing_indicators": indicators,
                "escalation_level": "CRITICAL"
            }

        # 2. Empathetic validation & Cognitive Reframing
        response_parts = []
        if is_hindi:
            response_parts.append(
                "Aapki baat sunkar dukh hua. Online harassment aur abusive messages jhelna bohot thaka dene wala aur distressing hota hai. "
                "Yeh baat hamesha yaad rakhiye ki doosron ke hateful comments ya dhamkiyan unki gandagi darshati hain, aapki worth nahi."
            )
        else:
            response_parts.append(
                "Thank you for reaching out and sharing that with me. Facing online hostility and abusive messages is exhausting and distressing. "
                "Please remember that other people's abusive behavior reflects on them, not on your personal worth or dignity."
            )

        if incident_context and incident_context.get("primary_class"):
            cb_class = incident_context['primary_class']
            if is_hindi:
                response_parts.append(f"\nDetect kiya gaya behavior **{cb_class}** category mein aata hai. Humara sabse bada focus aapki safety aur evidence preserve karna hai.")
            else:
                response_parts.append(f"\nBased on the detected **{cb_class}** behavior, our top priority is ensuring your safety and securing evidence.")

        # 3. Grounded Knowledge Base Guidance
        if rag_docs:
            for doc in rag_docs:
                if doc["type"] == "guide":
                    lines = [ln.strip() for ln in doc["content"].split("\n") if ln.strip() and not ln.startswith("#")]
                    summary = " ".join(lines[:2])
                    response_parts.append(f"\n**{doc['title']}:** {summary}")
                elif doc["type"] == "resource":
                    response_parts.append(f"\n**Official Helpline:** {doc['content']}")

        # 4. Clear Action Steps (Multilingual)
        if is_hindi:
            response_parts.append(
                "\n\n**Aapke liye zaroori steps:**\n"
                "1. **Retaliate mat kijiye:** Abuser ko gaali ya counter-threat mat dijiye; chupchap evidence collect karein.\n"
                "2. **Full Screenshot lein:** Chats, profile links, handles aur timestamp ke uncropped screenshots preserve karein.\n"
                "3. **Block aur Report:** Platform ke trust & safety option se account ko report aur block karein.\n"
                "4. **Police / 1930 Portal:** Agar personal data leak, blackmail ya physical harm ki dhamki ho, turant **cybercrime.gov.in** par report karein ya **1930** helpline par call karein."
            )
        else:
            response_parts.append(
                "\n\n**Recommended Action Steps:**\n"
                "1. **Do not retaliate or engage** with the abusive party.\n"
                "2. **Take uncropped screenshots** showing timestamps, profile handles, and URLs.\n"
                "3. **Block and report** the account using platform tools.\n"
                "4. If extortion, doxxing, or threats of harm occurred, immediately report to **cybercrime.gov.in** or call **1930** (National Cyber Crime Helpline)."
            )

        return {
            "response": " ".join(response_parts),
            "rag_sources": sources_used,
            "wellbeing_indicators": indicators,
            "escalation_level": indicators["escalation_urgency"]
        }

_agent_instance = None

def get_support_agent() -> SupportAIAgent:
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = SupportAIAgent()
    return _agent_instance
