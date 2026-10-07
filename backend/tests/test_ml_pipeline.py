from ml.inference.pipeline import get_ml_pipeline
from ml.preprocessing.normalizer import normalize_text, extract_tokens
from ml.preprocessing.language_detector import LanguageDetector

def test_language_detection():
    detector = LanguageDetector()
    lang_en, _ = detector.detect("You are completely useless.")
    assert lang_en == "English"

    lang_hi, _ = detector.detect("तुम बहुत बेकार हो।")
    assert lang_hi == "Hindi"

    lang_hinglish, _ = detector.detect("Tu kitna bada kutta hai bhai.")
    assert lang_hinglish == "Hinglish"

def test_normalization():
    raw = "Soooooo baaaad @bully https://spam.com 😡🤡"
    cleaned = normalize_text(raw)
    assert "@bully" not in cleaned
    assert "https://" not in cleaned
    assert "angry_face" in cleaned or "clown_mockery" in cleaned

def test_end_to_end_inference():
    pipeline = get_ml_pipeline()
    result = pipeline.analyze_text("Look at your face, you are so ugly.")
    assert "predicted_class" in result
    assert "confidence" in result
    assert "probabilities" in result
    assert "explanation" in result
    assert len(result["probabilities"]) == 10
    assert result["is_cyberbullying"] is True
    assert "ugly" in [t.lower() for t in result["important_tokens"]]

def test_clean_text_inference():
    pipeline = get_ml_pipeline()
    result = pipeline.analyze_text("Good morning, have a wonderful and productive day!")
    assert result["predicted_class"] == "Non-cyberbullying"
    assert result["is_cyberbullying"] is False
