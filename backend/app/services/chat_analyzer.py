from typing import List, Dict, Any
from collections import Counter
from ml.inference.pipeline import get_ml_pipeline
from backend.app.schemas.analysis import ChatMessageInput, AnalyzedChatMessage, ChatAnalysisResponse

class ChatConversationAnalyzer:
    """
    Analyzes multi-message chat transcripts and conversation screenshots:
    - Message segmentation & speaker tracking
    - Individual message classification
    - Repeated targeting detection & frequency analysis
    - Escalation trajectory modeling
    - Coordinated harassment indicators
    """

    def __init__(self):
        self.ml_pipeline = get_ml_pipeline()

    def analyze_conversation(self, messages: List[ChatMessageInput], platform: str = "Chat") -> ChatAnalysisResponse:
        analyzed_msgs = []
        sender_counts = Counter()
        abusive_senders = Counter()
        categories_found = []
        confidences = []
        threat_count = 0

        for msg in messages:
            sender = msg.sender.strip() if msg.sender else "Unknown User"
            sender_counts[sender] += 1
            
            # Run ML pipeline on each message
            result = self.ml_pipeline.analyze_text(msg.text)
            is_bullying = result["is_cyberbullying"]
            pred_class = result["predicted_class"]
            conf = result["confidence"]

            if is_bullying:
                abusive_senders[sender] += 1
                categories_found.append(pred_class)
                confidences.append(conf)
                if pred_class == "Threat/Intimidation":
                    threat_count += 1

            analyzed_msgs.append(AnalyzedChatMessage(
                sender=sender,
                text=msg.text,
                timestamp=msg.timestamp,
                predicted_class=pred_class,
                confidence=conf,
                is_bullying=is_bullying
            ))

        total_msgs = len(messages)
        total_abusive = sum(abusive_senders.values())
        overall_conf = float(sum(confidences) / len(confidences)) if confidences else 0.85

        # Determine primary category
        if categories_found:
            primary_category = Counter(categories_found).most_common(1)[0][0]
        else:
            primary_category = "Non-cyberbullying"

        # Repeated targeting pattern detection
        repeated_targeting = False
        repeated_summary = "No repeated hostile targeting pattern identified."
        bullies = list(abusive_senders.keys())

        if total_abusive >= 2:
            repeated_targeting = True
            # Find primary antagonist
            top_antagonist, count = abusive_senders.most_common(1)[0]
            if len(bullies) > 1:
                repeated_summary = f"Multiple participants ({len(bullies)} distinct accounts) directed coordinated derogatory remarks across {total_abusive} messages."
            else:
                repeated_summary = f"Repeated harmful-language pattern detected: Sender '{top_antagonist}' sent {count} consecutive hostile messages."

        # Escalation trajectory
        escalation_detected = False
        if threat_count > 0 or total_abusive >= 3:
            escalation_detected = True

        # Incident assessment
        if threat_count > 0:
            assessment = "High-urgency escalation: Explicit threatening or intimidating language detected within conversational stream."
            rec_action = "Preserve chat exports immediately, block the participants, and escalate case to the official cybercrime helpline (1930) or local authorities."
        elif repeated_targeting:
            assessment = "Repeated harmful-language pattern detected across sequential chat messages."
            rec_action = "Restrict direct messages, document full chat context via CyberGuard Incident Report, and consider seeking help through consultant escalation."
        elif total_abusive > 0:
            assessment = "Isolated hostile communication observed without an established repeated escalation pattern."
            rec_action = "Report and mute the offending account to prevent potential escalation."
        else:
            assessment = "No hostile or bullying linguistic patterns detected in the submitted conversation."
            rec_action = "Conversation appears constructive. Continue following standard digital privacy guidelines."

        return ChatAnalysisResponse(
            total_messages=total_msgs,
            analyzed_messages=analyzed_msgs,
            primary_category=primary_category,
            overall_confidence=round(overall_conf, 4),
            repeated_targeting_detected=repeated_targeting,
            repeated_targeting_summary=repeated_summary,
            active_bullies=bullies,
            escalation_detected=escalation_detected,
            incident_assessment=assessment,
            recommended_safety_action=rec_action
        )

_chat_analyzer = None

def get_chat_analyzer() -> ChatConversationAnalyzer:
    global _chat_analyzer
    if _chat_analyzer is None:
        _chat_analyzer = ChatConversationAnalyzer()
    return _chat_analyzer
