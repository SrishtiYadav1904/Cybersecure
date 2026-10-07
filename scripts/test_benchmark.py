import sys
from pathlib import Path

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ml.inference.pipeline import CyberGuardMLPipeline

def run_tests():
    pipeline = CyberGuardMLPipeline()

    test_cases = [
        "I will rape you",
        "moti bhaisn marr jaa",
        "tu chutiya hai",
        "tu bahut gandi hai",
        "mar ja",
        "main tujhe maar dunga",
        "I will hunt you down and beat you senseless.",
        "घर से बाहर निकल, तुझे जान से मार दूंगा आज।",
        "Thank you so much for explaining the code, really helpful project!",
        "Bhai project submit ho gaya, thanks for helping me out yaar!",
        "आज का मौसम बहुत सुहावना है और शाम को हल्की बारिश हो रही है।"
    ]

    print(f"=== Testing {len(test_cases)} Benchmark Sentences ===\n")
    for text in test_cases:
        res = pipeline.analyze_text(text)
        print(f"Text:       \"{text}\"")
        print(f"Label:      {res['predicted_class']} (Cyberbullying: {res['is_cyberbullying']}, Severity: {res['severity']})")
        print(f"Confidence: {res['confidence'] * 100:.2f}% | Lang: {res['detected_language']}")
        print(f"Tokens:     {res.get('important_tokens', [])}")
        top3_probs = [(p['category'], round(p['probability'], 3)) for p in res.get('probabilities', [])[:3]]
        print(f"Top-3:      {top3_probs}")
        print("-" * 60)

if __name__ == "__main__":
    run_tests()
