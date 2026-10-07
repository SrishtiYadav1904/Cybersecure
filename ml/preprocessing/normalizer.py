import re
import unicodedata
from typing import List

# Common Hinglish and internet slang canonicalization map
SLANG_CANONICAL_MAP = {
    # Threats & violence
    "marr": "mar",
    "mrr": "mar",
    "jaa": "ja",
    "marrja": "mar ja",
    "marja": "mar ja",
    "maardunga": "maar dunga",
    "mardunga": "maar dunga",
    "maarenge": "marenge",
    "khatamkar": "khatam kar",
    
    # Body & Appearance
    "bhaisn": "bhains",
    "bhens": "bhains",
    "bhainse": "bhains",
    "motii": "moti",
    "motaa": "mota",
    "badsurat": "badsurat",
    "badsoorat": "badsurat",
    "suarr": "suar",
    
    # Insults & Profanity
    "chutya": "chutiya",
    "chootiya": "chutiya",
    "chutiye": "chutiya",
    "ctya": "chutiya",
    "mc": "madarchod",
    "maderchod": "madarchod",
    "bc": "behenchod",
    "bhenchod": "behenchod",
    "behnchod": "behenchod",
    "bsdk": "bhosdike",
    "saale": "sale",
    "kaminaa": "kamina",
    "kaminey": "kamina",
    "harami": "harami",
    "kuttaa": "kutta",
    "kutte": "kutta",
    "gandi": "gandi",
    "ganda": "ganda",
    "gande": "ganda",
    
    # Gender & Slurs
    "randi": "randi",
    "rndi": "randi",
    "raand": "randi",
    "chudail": "chudail",
    
    # Leetspeak variations
    "r4pe": "rape",
    "raep": "rape",
    "k!ll": "kill",
    "k1ll": "kill",
    "b!tch": "bitch",
    "b1tch": "bitch",
    "f*ck": "fuck",
    "sh*t": "shit"
}

# Emoji sentiment mappings
EMOJI_DESCRIPTIONS = {
    "😡": " angry_face ",
    "🤬": " swearing_face ",
    "🤡": " clown_mockery ",
    "🤮": " vomiting_disgust ",
    "💩": " poop_insult ",
    "💀": " skull_threat ",
    "🖕": " middle_finger ",
    "👎": " thumbs_down ",
    "😭": " crying ",
    "❤️": " love ",
    "👍": " thumbs_up ",
    "🙏": " folded_hands "
}

def clean_unicode(text: str) -> str:
    """Normalize unicode characters (e.g. Devanagari NFC form) and strip dandas."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    text = text.replace('।', ' ').replace('॥', ' ')
    return text

def replace_emojis(text: str) -> str:
    """Replace common social media emojis with descriptive tokens."""
    for emoji_char, token in EMOJI_DESCRIPTIONS.items():
        text = text.replace(emoji_char, token)
    return text

def normalize_leetspeak(text: str) -> str:
    """Normalize common leetspeak character substitutions."""
    # Obfuscated symbols within letters
    text = re.sub(r'(?<=[a-zA-Z])[@4](?=[a-zA-Z])', 'a', text)
    text = re.sub(r'(?<=[a-zA-Z])[!1](?=[a-zA-Z])', 'i', text)
    text = re.sub(r'(?<=[a-zA-Z])0(?=[a-zA-Z])', 'o', text)
    text = re.sub(r'(?<=[a-zA-Z])\$(?=[a-zA-Z])', 's', text)
    return text

def reduce_repeated_characters(text: str) -> str:
    """
    Transform exaggerated character repetitions:
    e.g. 'sooooo baaaaad' -> 'so baad', 'marrrrr' -> 'mar'
    """
    return re.sub(r'(.)\1{2,}', r'\1', text)

def canonicalize_slang_tokens(text: str) -> str:
    """Apply dictionary-based canonicalization to normalize slang and colloquial forms."""
    words = text.split()
    normalized_words = []
    for w in words:
        w_clean = re.sub(r'[^\w]', '', w.lower())
        if w_clean in SLANG_CANONICAL_MAP:
            normalized_words.append(SLANG_CANONICAL_MAP[w_clean])
        else:
            normalized_words.append(w)
    return ' '.join(normalized_words)

def normalize_text(text: str) -> str:
    """
    Complete text normalization pipeline:
    1. Unicode normalization and Devanagari cleanup
    2. Emoji translation
    3. Leetspeak de-obfuscation
    4. URL and handle masking
    5. Repeated character reduction
    6. Slang canonicalization
    7. Whitespace trimming
    """
    if not text or not isinstance(text, str):
        return ""
    
    # 1. Unicode
    text = clean_unicode(text)
    
    # 2. Emoji translation
    text = replace_emojis(text)
    
    # 3. Leetspeak
    text = normalize_leetspeak(text)
    
    # 4. Mask URLs and handles
    text = re.sub(r'https?://\S+|www\.\S+', ' <URL> ', text)
    text = re.sub(r'@\w+', ' <USER> ', text)
    
    # 5. Repeated chars (reduce 3+ down to 1)
    text = reduce_repeated_characters(text)
    
    # 6. Canonicalize slang
    text = canonicalize_slang_tokens(text)
    
    # 7. Clean extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_tokens(text: str) -> List[str]:
    """Tokenize text into lowercase alphanumeric and Devanagari words without punctuation."""
    cleaned = normalize_text(text)
    raw_tokens = re.findall(r'[\u0900-\u097F\w]+', cleaned.lower())
    clean_tokens = [t.strip('।॥.,!?;:()[]{}"\'') for t in raw_tokens if t.strip('।॥.,!?;:()[]{}"\'')]
    return clean_tokens
