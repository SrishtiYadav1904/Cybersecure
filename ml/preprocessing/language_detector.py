import re
from typing import Dict, Tuple

# Common Hindi stopwords and markers in Latin script (Hinglish)
HINGLISH_MARKERS = {
    "hai", "ho", "hoon", "nahi", "nhi", "kaise", "kya", "kyun", "bhai", "yaar",
    "tera", "teri", "tere", "mera", "meri", "mere", "apna", "apni", "wala", "wali",
    "wale", "hoga", "hogi", "raha", "rahi", "rahe", "karo", "karna", "baat",
    "bhi", "yeh", "woh", "isko", "usko", "sab", "kuch", "aisa", "aise", "tu",
    "sale", "saale", "kamina", "pagal", "bkl", "mc", "bc", "chutiya", "gandu", "moti",
    "bhaisn", "marr", "jaa", "kutta", "kamine", "harami", "dost", "dunga", "karu",
    "varna", "baith", "pel", "chup", "chap", "dhamki", "khatam"
}

# Devanagari character range
DEVANAGARI_REGEX = re.compile(r'[\u0900-\u097F]')

class LanguageDetector:
    """
    Multilingual detector supporting:
    - Hindi (Devanagari script)
    - Hinglish (Romanized Hindi code-mixed)
    - English (Standard Latin script)
    """

    def detect(self, text: str) -> Tuple[str, float]:
        """
        Returns (detected_language, confidence)
        """
        if not text or not text.strip():
            return "English", 0.50

        # Check for Devanagari characters
        devanagari_chars = DEVANAGARI_REGEX.findall(text)
        total_alpha_chars = len(re.findall(r'[a-zA-Z\u0900-\u097F]', text))

        if total_alpha_chars > 0 and len(devanagari_chars) / total_alpha_chars >= 0.35:
            conf = min(0.98, 0.70 + (len(devanagari_chars) / total_alpha_chars) * 0.28)
            return "Hindi", round(conf, 4)

        # Tokenize lowercase latin words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        if not words:
            return "English", 0.50

        hinglish_hits = sum(1 for w in words if w in HINGLISH_MARKERS)
        hinglish_ratio = hinglish_hits / len(words)

        if hinglish_hits >= 1 or hinglish_ratio >= 0.15:
            conf = min(0.96, 0.70 + hinglish_ratio * 0.25)
            return "Hinglish", round(conf, 4)

        # Default to English
        return "English", 0.92

    def get_details(self, text: str) -> Dict[str, any]:
        lang, conf = self.detect(text)
        return {
            "detected_language": lang,
            "confidence": conf,
            "is_code_mixed": lang == "Hinglish"
        }
