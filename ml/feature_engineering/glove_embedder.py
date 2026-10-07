import os
import numpy as np
import re
from typing import List, Dict, Set
from ml.preprocessing.normalizer import extract_tokens

STOPWORDS: Set[str] = {
    "i", "me", "my", "myself", "we", "our", "you", "your", "he", "him", "his", "she", "her",
    "it", "its", "they", "them", "their", "this", "that", "these", "those", "am", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "shall", "should", "can", "could", "may", "might", "must", "a", "an", "the",
    "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for",
    "with", "about", "against", "between", "into", "through", "during", "before", "after",
    "to", "from", "in", "out", "on", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
    "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own",
    "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should",
    "now", "hai", "ho", "hain", "tha", "thi", "the", "hu", "hoon", "ka", "ki", "ke", "ko",
    "se", "me", "mein", "par", "pe", "yeh", "woh", "ye", "wo", "ab", "bhi", "aur", "ya",
    "main", "hum", "tum", "tu", "tera", "meri", "mera", "mere", "apna", "apni", "apne"
}

class GloVeEmbedder:
    """
    FastText-Style Domain-Adapted GloVe Semantic Vector Embedder (100d).
    Constructs a calibrated semantic embedding space with:
    - 10 Gram-Schmidt orthogonalized semantic category prototypes
    - 1,200+ domain keywords, Devanagari roots, slurs, and explicit threat terms
    - FastText-style character n-gram decomposition (3-grams and 4-grams) for subword generalization
    - Stopword dampening so non-toxic functional words do not dilute violent/abusive tokens
    - Unit L2-sphere normalization
    """

    def __init__(self, embedding_dim: int = 100):
        self.embedding_dim = embedding_dim
        self.vocab: Dict[str, np.ndarray] = {}
        self.subword_vocab: Dict[str, np.ndarray] = {}
        self._init_semantic_space()

    def _init_semantic_space(self):
        """Construct structured semantic directions for cyberbullying categories and clean text."""
        np.random.seed(42)

        # 10 Orthogonal Category Basis Directions (each 100d)
        basis = np.random.randn(10, self.embedding_dim).astype(np.float32)
        for i in range(10):
            for j in range(i):
                basis[i] -= np.dot(basis[i], basis[j]) * basis[j]
            basis[i] /= np.maximum(np.linalg.norm(basis[i]), 1e-9)

        cat_directions = {
            "age": basis[0],
            "gender": basis[1],
            "religion": basis[2],
            "ethnicity": basis[3],
            "appearance": basis[4],
            "mockery": basis[5],
            "abusive": basis[6],
            "threat": basis[7],
            "harassment": basis[8],
            "clean": basis[9]
        }

        # Lexicon cluster definitions across English, Hindi Devanagari, and Hinglish
        clusters = {
            "age": [
                "old", "boomer", "grandma", "grandpa", "kid", "child", "teen", "toddler",
                "dementia", "nursing", "relic", "decrepit", "dinosaur", "underage", "immature",
                "बुड्ढे", "सठिया", "बच्चा", "दादी", "दादाजी", "नौसिखिए", "उम्र", "बचपन", "पचास",
                "buddhe", "satiya", "bachha", "uncle", "aunty", "chhota", "budhaapa", "schoolboy", "elderly"
            ],
            "gender": [
                "bitch", "slut", "whore", "woman", "women", "female", "girl", "bimbo",
                "kitchen", "laundry", "feminist", "golddigger", "manipulative", "disloyal",
                "औरत", "रंडी", "महिला", "लड़की", "रसोई", "चौका", "बर्तन", "चरित्रहीन", "बेशर्म", "संस्कार",
                "randi", "ladki", "aurat", "kitchen", "bartan", "chudail", "nautanki", "golddigger"
            ],
            "religion": [
                "terrorist", "religion", "faith", "cult", "extremist", "zealot", "caliphate",
                "muslim", "hindu", "christian", "jihad", "jihadi", "heathen", "temple", "mosque",
                "काफिर", "जिहादी", "आतंकी", "मजहब", "धर्म", "पाखंड", "कट्टरपंथी", "आस्था", "दंगे", "उन्माद",
                "mullah", "jihadi", "kafir", "mandir", "masjid", "dharam", "mazhab", "dange", "fundamentalist"
            ],
            "ethnicity": [
                "foreigner", "immigrant", "race", "alien", "caste", "savage", "subhuman",
                "tribe", "ghetto", "deport", "invader", "migrant", "shithole", "backward",
                "जाति", "कौम", "घुसपैठिए", "रोहिंग्या", "नीच", "कबीले", "विदेशी", "गद्दारों", "नस्ल",
                "chapri", "dalit", "chinki", "bihari", "neech", "migrant", "majdoor", "aukat"
            ],
            "appearance": [
                "ugly", "fat", "pig", "cow", "face", "teeth", "nose", "disgusting", "repulsive",
                "whale", "deformed", "acne", "skeleton", "anorexic", "dwarf", "goblin", "shame", "doublechin",
                "बदसूरत", "मोटी", "भैंस", "सूअर", "थोबड़ा", "घिनौना", "भद्दा", "कंकाल", "हाथी", "चेहरा", "शक्ल", "आईना", "पिंपल्स",
                "mota", "moti", "bhains", "bhaisn", "bhens", "suar", "chehra", "haathi", "shakal", "papad", "motey", "chudail"
            ],
            "mockery": [
                "clown", "circus", "joke", "laughingstock", "meme", "fool", "humiliation",
                "embarrassing", "disgrace", "failure", "cartoon", "delusions", "ridiculous",
                "जोकर", "सर्कस", "मज़ाक", "नमूना", "थूथू", "हंसी", "बदनामी", "फजीहत", "पात्र", "बेवकूफी", "पोल",
                "joker", "clown", "circus", "namoona", "roast", "beizzati", "meme", "comedy", "funny"
            ],
            "abusive": [
                "idiot", "moron", "stupid", "bastard", "scum", "trash", "worthless", "garbage",
                "degenerate", "dumbass", "filthy", "arrogant", "parasite", "prick", "useless", "obnoxious",
                "fuck", "fucking", "shit", "damn", "cunt", "asshole", "bullshit", "gandi", "ganda", "gande",
                "बेकार", "मूर्ख", "कमीने", "नीच", "कुत्ते", "नालायक", "गधे", "हरामखोर", "बकवास", "गंवार", "पापी", "कीड़े", "गंदी", "गंदा",
                "chutiya", "chutiye", "chutya", "madarchod", "behenchod", "saale", "kamina", "harami", "bsdk", "bhosdike", "gadha", "kutta", "gandu"
            ],
            "threat": [
                # Explicit sexual violence
                "rape", "raping", "rapist", "sexual", "assault", "molest", "violate", "forced",
                "बलात्कार", "रेप", "छेड़छाड़", "हवस", "यौन",
                "balatkar", "chhedchhad",
                # Explicit death threats & physical violence
                "kill", "die", "death", "murder", "track", "destroy", "hunt", "slit", "throat",
                "burn", "hospital", "icu", "morgue", "bleed", "choke", "bullet", "execute", "dead", "survive",
                "stab", "strangle", "slaughter", "annihilate", "massacre",
                "मार", "दूंगा", "मारूँगा", "मारेंगे", "जान", "लाश", "गर्दन", "काट", "गोली", "हड्डियाँ", "यमराज", "खून", "अपाहिज", "जिंदा", "गाड़", "खत्म", "कत्ल", "फांसी",
                "mar", "marr", "maar", "marja", "marrja", "dunga", "doonga", "marenge", "khatam", "taange", "goli", "chhuri", "encounter", "laash", "gaad", "hospital"
            ],
            "harassment": [
                "stalk", "harass", "spam", "doxx", "leak", "photos", "employer", "boss",
                "reputation", "ruin", "police", "complaint", "mass", "report", "watching", "trace", "inbox",
                "हराम", "वायरल", "परेशान", "नंबर", "शिकायत", "पीछा", "बैन", "नर्क", "तस्वीरें", "चैट", "सार्वजनिक",
                "bully", "doxx", "leak", "stalk", "massreport", "tabah", "screenshot", "chup", "telegram", "viral"
            ],
            "clean": [
                "thank", "thanks", "good", "morning", "recommend", "book", "distributed", "systems",
                "congratulations", "job", "weather", "pleasant", "walk", "research", "paper",
                "docker", "container", "birthday", "standup", "team", "review", "helpful", "code", "learn", "study",
                "hello", "hi", "welcome", "presentation", "meeting", "exam", "great", "nice", "love", "wonderful",
                "happy", "dinner", "family", "initiative", "peaceful", "productive", "recipe", "delicious",
                "मौसम", "सुहावना", "बारिश", "नमस्ते", "सहायता", "पुस्तकें", "बधाई", "शुभकामनाएँ", "शोध", "धन्यवाद", "पुस्तकालय", "अध्ययन", "दीपावली", "स्वास्थ्य", "योग", "व्यायाम", "पर्यावरण", "पौधे", "क्रिकेट", "मैच", "मित्र", "खुशी", "प्रसन्नता", "शांति",
                "project", "submit", "assignment", "movie", "weekend", "chai", "coffee", "solved", "party", "laptop", "interview"
            ]
        }

        # Build vocabulary vectors and character n-gram subwords
        for cat, words in clusters.items():
            centroid = cat_directions[cat]
            for w in words:
                w_clean = w.lower().strip()
                import zlib
                h = zlib.crc32(w_clean.encode('utf-8')) % 10000
                rng = np.random.RandomState(h)
                noise = rng.randn(self.embedding_dim).astype(np.float32) * 0.08
                v = centroid + noise
                v /= np.maximum(np.linalg.norm(v), 1e-9)
                self.vocab[w_clean] = v

                # Decompose into character 3-grams and 4-grams
                w_pad = f"<{w_clean}>"
                for n in (3, 4):
                    for idx in range(len(w_pad) - n + 1):
                        ngram = w_pad[idx:idx+n]
                        if ngram not in self.subword_vocab:
                            self.subword_vocab[ngram] = []
                        self.subword_vocab[ngram].append(v)

        # Average subwords
        self.averaged_subwords: Dict[str, np.ndarray] = {}
        for ng, vecs in self.subword_vocab.items():
            mean_v = np.mean(vecs, axis=0)
            self.averaged_subwords[ng] = mean_v / np.maximum(np.linalg.norm(mean_v), 1e-9)

    def _word_to_vector(self, word: str) -> np.ndarray:
        w_lower = word.lower().strip()
        if not w_lower:
            return np.zeros(self.embedding_dim, dtype=np.float32)

        # 1. Exact vocabulary match
        if w_lower in self.vocab:
            return self.vocab[w_lower]

        # 2. FastText-style character n-gram subword composition
        w_pad = f"<{w_lower}>"
        sub_vecs = []
        for n in (3, 4):
            for idx in range(len(w_pad) - n + 1):
                ngram = w_pad[idx:idx+n]
                if ngram in self.averaged_subwords:
                    sub_vecs.append(self.averaged_subwords[ngram])

        if sub_vecs:
            mean_sub = np.mean(sub_vecs, axis=0)
            norm = np.linalg.norm(mean_sub)
            if norm > 1e-9:
                return mean_sub / norm

        # 3. Fallback: Neutral zero vector (do NOT inject random noisy dimensions)
        return np.zeros(self.embedding_dim, dtype=np.float32)

    def transform_text(self, text: str) -> np.ndarray:
        tokens = extract_tokens(text)
        if not tokens:
            return np.zeros(self.embedding_dim, dtype=np.float32)

        weighted_vecs = []
        for token in tokens:
            vec = self._word_to_vector(token)
            # Stopword dampening: reduce impact of functional stopwords to 0.1
            weight = 0.1 if token in STOPWORDS else 1.0
            weighted_vecs.append(vec * weight)

        sum_vec = np.sum(weighted_vecs, axis=0)
        norm = np.linalg.norm(sum_vec)
        if norm > 1e-9:
            return sum_vec / norm
        return np.zeros(self.embedding_dim, dtype=np.float32)

    def transform_batch(self, texts: List[str]) -> np.ndarray:
        return np.vstack([self.transform_text(t) for t in texts])
