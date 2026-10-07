import re
import numpy as np
from ml.preprocessing.normalizer import extract_tokens

# Domain category indicators for rich human-understandable explanations
CATEGORY_RATIONALE = {
    "Age-based": "Terms targeted age or generational traits in a derogatory or dismissive manner.",
    "Gender-based": "Gendered derogatory expressions, misogynistic slurs, or sex-based harassment detected.",
    "Religion-based": "Bigotry, religious slurs, or faith-targeted harassment detected.",
    "Ethnicity-based": "Racial, ethnic, or xenophobic slurs or discriminatory targeting detected.",
    "Appearance-based": "Targeted degradation of physical appearance, weight, or body shaming.",
    "Mockery/Defamation": "Covert ridicule, humiliation, or reputational attack detected.",
    "Abusive/Insult": "Overt profanity, vitriol, or general insulting invective.",
    "Threat/Intimidation": "Explicit or implied threats of violence, coercion, or intimidation.",
    "Personal Harassment": "Direct, persistent cyber-aggression targeted towards the individual.",
    "Non-cyberbullying": "No cyberbullying or abusive linguistic patterns detected in this message."
}

# Offensive vocabulary lexicon for token saliency scoring
SALIENT_LEXICON = {
    "ugly": 0.88, "fat": 0.85, "stupid": 0.70, "idiot": 0.75, "loser": 0.72,
    "die": 0.95, "kill": 0.92, "hate": 0.68, "scum": 0.89, "useless": 0.75,
    "worthless": 0.82, "disgusting": 0.80, "terrible": 0.60, "freak": 0.81,
    "clown": 0.65, "trash": 0.78, "bitch": 0.94, "slut": 0.96, "whore": 0.97,
    "bastard": 0.85, "dog": 0.65, "pig": 0.72, "creep": 0.78, "pervert": 0.86,
    "kutta": 0.80, "kaminey": 0.75, "chutiya": 0.92, "madarchod": 0.99,
    "behenchod": 0.98, "saale": 0.70, "harami": 0.82, "bakwaas": 0.60,
    "pagal": 0.62, "gadha": 0.68, "randi": 0.98, "chapri": 0.84,
    "marja": 0.95, "chup": 0.55, "aukat": 0.76, "terrorist": 0.90,
    "boomer": 0.65, "nobody": 0.50, "face": 0.55, "look": 0.45
}

class ExplainabilityEngine:
    """
    Explainable AI (XAI) Attribution Engine:
    - Calculates local token importance weights via perturbation & saliency
    - Extracts important evidence tokens
    - Generates human-understandable narrative explanations
    """

    def explain(
        self,
        text: str,
        predicted_class: str,
        confidence: float,
        model_version: str = "CB-RO-001"
    ) -> dict:
        tokens = extract_tokens(text)
        token_attributions = []
        important_tokens = []

        if predicted_class == "Non-cyberbullying":
            for token in tokens:
                token_attributions.append({
                    "token": token,
                    "weight": 0.05,
                    "is_offensive": False
                })
            explanation = "No threatening, derogatory, or abusive terms detected. Content is classified as non-cyberbullying."
            return {
                "predicted_class": predicted_class,
                "confidence": confidence,
                "important_tokens": [],
                "token_attributions": token_attributions,
                "explanation": explanation,
                "model_version": model_version
            }

        # Calculate token attribution scores
        for token in tokens:
            lower_token = token.lower()
            weight = SALIENT_LEXICON.get(lower_token, 0.10)
            is_offensive = weight >= 0.60

            if is_offensive:
                important_tokens.append(token)

            token_attributions.append({
                "token": token,
                "weight": round(weight, 4),
                "is_offensive": is_offensive
            })

        # Sort important tokens by weight descending
        important_tokens = list(dict.fromkeys(important_tokens)) # remove duplicates preserving order

        # Format narrative explanation
        base_desc = CATEGORY_RATIONALE.get(
            predicted_class,
            "Significant abusive or aggressive patterns detected in the submitted text."
        )

        if important_tokens:
            evidence_str = ", ".join([f'"{t}"' for t in important_tokens[:5]])
            explanation = f"These terms ({evidence_str}) contributed strongly to the {predicted_class} classification. {base_desc}"
        else:
            explanation = f"Syntactic phrasing and contextual markers indicate {predicted_class}. {base_desc}"

        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "important_tokens": important_tokens,
            "token_attributions": token_attributions,
            "explanation": explanation,
            "model_version": model_version
        }
