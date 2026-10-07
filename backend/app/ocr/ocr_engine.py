import os
import io
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from typing import Tuple, Dict, Any, List

class OCREngine:
    """
    Multilingual Deep Learning OCR Engine:
    - Preprocessing: Resolution upscaling, grayscale, CLAHE adaptive contrast, bilateral denoising
    - Engine: RapidOCR (ONNX Runtime, DBNet text detection + SVTR/CRNN text recognition)
    - Spatial line reconstruction (top-to-bottom, left-to-right)
    - Support for English, Hindi (Devanagari), and Hinglish (Roman script)
    - Zero fake heuristics: if an image has no text, returns empty string and 0.0 confidence.
    """

    def __init__(self):
        self.backend = None
        self._init_ocr()

    def _init_ocr(self):
        # 1. Try RapidOCR (Primary, fast ONNX runtime deep learning engine)
        try:
            from rapidocr_onnxruntime import RapidOCR
            self.rapid_ocr = RapidOCR()
            self.backend = "rapidocr"
            return
        except Exception:
            pass

        # 2. Try EasyOCR
        try:
            import easyocr
            self.easy_reader = easyocr.Reader(['en', 'hi'], gpu=False)
            self.backend = "easyocr"
            return
        except Exception:
            pass

        # 3. Try PyTesseract
        try:
            import pytesseract
            self.tesseract = pytesseract
            self.backend = "pytesseract"
            return
        except Exception:
            pass

        self.backend = "none"

    def preprocess_image_cv2(self, image_bytes: bytes) -> np.ndarray:
        """
        Comprehensive OCR preprocessing pipeline:
        1. Decode image bytes to OpenCV BGR
        2. Resolution check & optional adaptive upscaling if small (< 800px)
        3. Convert to grayscale
        4. CLAHE (Contrast Limited Adaptive Histogram Equalization)
        5. Bilateral filter for edge-preserving denoising
        """
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            # Fallback using PIL
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        h, w = img.shape[:2]

        # 1. Resolution Check & Adaptive Upscaling
        if max(h, w) < 800:
            scale = 800.0 / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_LANCZOS4)

        # 2. Grayscale conversion
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 3. Contrast enhancement via CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # 4. Edge-preserving bilateral filter for noise suppression
        denoised = cv2.bilateralFilter(enhanced, d=5, sigmaColor=50, sigmaSpace=50)

        return denoised

    def extract_text_from_bytes(self, image_bytes: bytes, filename: str = "") -> Tuple[str, float]:
        """
        Extract text and overall confidence from raw image bytes.
        Returns: (extracted_text, confidence_score)
        """
        res = self.extract_with_metadata(image_bytes, filename)
        return res["extracted_text"], res["confidence"]

    def extract_with_metadata(self, image_bytes: bytes, filename: str = "") -> Dict[str, Any]:
        """
        Execute full OCR pipeline returning bounding boxes, per-line confidence,
        reconstructed text, and execution metadata.
        """
        if not image_bytes:
            return {
                "extracted_text": "",
                "confidence": 0.0,
                "lines": [],
                "engine": self.backend,
                "word_count": 0
            }

        try:
            processed_img = self.preprocess_image_cv2(image_bytes)
        except Exception:
            return {
                "extracted_text": "",
                "confidence": 0.0,
                "lines": [],
                "engine": self.backend,
                "word_count": 0
            }

        lines_output = []

        if self.backend == "rapidocr":
            try:
                # RapidOCR accepts numpy image directly (BGR or Gray)
                result, elapse = self.rapid_ocr(processed_img)
                if result:
                    # Sort detected text boxes top-to-bottom, left-to-right
                    # result item: [box_coordinates, text, score]
                    sorted_res = sorted(result, key=lambda x: (x[0][0][1], x[0][0][0]))
                    for item in sorted_res:
                        txt = str(item[1]).strip()
                        score = float(item[2])
                        if txt:
                            lines_output.append({"text": txt, "confidence": round(score, 4), "box": item[0]})

            except Exception as e:
                pass

        elif self.backend == "easyocr":
            try:
                res = self.easy_reader.readtext(processed_img)
                # res: [(bbox, text, prob)]
                sorted_res = sorted(res, key=lambda x: (x[0][0][1], x[0][0][0]))
                for item in sorted_res:
                    lines_output.append({"text": str(item[1]).strip(), "confidence": round(float(item[2]), 4)})
            except Exception:
                pass

        elif self.backend == "pytesseract":
            try:
                data = self.tesseract.image_to_data(processed_img, output_type=self.tesseract.Output.DICT)
                n_boxes = len(data['text'])
                for i in range(n_boxes):
                    txt = data['text'][i].strip()
                    conf = float(data['conf'][i])
                    if txt and conf > 0:
                        lines_output.append({"text": txt, "confidence": round(conf / 100.0, 4)})
            except Exception:
                pass

        # Text reconstruction
        extracted_text = " ".join([l["text"] for l in lines_output]).strip()
        if lines_output:
            avg_conf = float(np.mean([l["confidence"] for l in lines_output]))
        else:
            avg_conf = 0.0

        return {
            "extracted_text": extracted_text,
            "confidence": round(avg_conf, 4),
            "lines": lines_output,
            "engine": self.backend,
            "word_count": len(extracted_text.split()) if extracted_text else 0
        }

# Global singleton OCR engine
_ocr_instance = None

def get_ocr_engine() -> OCREngine:
    global _ocr_instance
    if _ocr_instance is None:
        _ocr_instance = OCREngine()
    return _ocr_instance
