import pytesseract
import os
import sys

# Try to use EasyOCR if available, otherwise fallback to Tesseract
EASY_OCR_AVAILABLE = False
try:
    import easyocr
    EASY_OCR_AVAILABLE = True
    print("[OCR] [OK] EasyOCR available - High accuracy mode")
except Exception as e:
    # Catch ImportError, OSError, DLL errors, etc.
    EASY_OCR_AVAILABLE = False
    error_type = type(e).__name__
    print(f"[OCR] [WARNING] EasyOCR not available ({error_type}) - Using Tesseract")

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Lazy initialize EasyOCR reader
_reader = None

def get_reader():
    """Get or initialize EasyOCR reader (lazy loading)"""
    global _reader
    if _reader is None:
        try:
            import easyocr
            print("[OCR] Loading EasyOCR models (first time only)...")
            _reader = easyocr.Reader(['en', 'hi'], gpu=False)
        except Exception as e:
            print(f"[OCR] EasyOCR failed: {str(e)}")
            _reader = False
    return _reader if _reader != False else None

def extract_text(image):
    """
    Extract text from image using EasyOCR (primary) or Tesseract (fallback)
    EasyOCR: 95%+ accuracy
    Tesseract: 70-80% accuracy (fallback)
    """
    try:
        # Try EasyOCR first if available
        if EASY_OCR_AVAILABLE:
            reader = get_reader()
            if reader:
                try:
                    # Read text using EasyOCR
                    results = reader.readtext(image, detail=0)  # detail=0 returns text only
                    
                    # Join all detected text
                    text = '\n'.join(results)
                    
                    if not text.strip():
                        return "[No text detected]"
                    
                    print("[OCR] [OK] EasyOCR extraction successful")
                    return text
                except Exception as e:
                    print(f"[OCR] EasyOCR error: {str(e)}")
                    print("[OCR] Falling back to Tesseract...")
        
        # Fallback to Tesseract
        print("[OCR] Using Tesseract OCR")
        text = pytesseract.image_to_string(image)
        return text if text.strip() else "[No text detected]"
        
    except Exception as e:
        print(f"[OCR] Error extracting text: {str(e)}")
        return f"[Error: {str(e)}]"

def extract_text_with_confidence(image):
    """
    Extract text with confidence scores
    Only works with EasyOCR
    """
    try:
        if EASY_OCR_AVAILABLE:
            reader = get_reader()
            if reader:
                results = reader.readtext(image, detail=1)  # detail=1 returns text + confidence
                
                formatted_results = []
                for detection in results:
                    text = detection[1]
                    confidence = detection[2]
                    formatted_results.append({
                        'text': text,
                        'confidence': round(confidence, 3),
                        'bbox': detection[0]  # Bounding box coordinates
                    })
                
                return formatted_results
        
        # Fallback: return simple results from Tesseract
        text = pytesseract.image_to_string(image)
        return [{'text': text, 'confidence': 0.8}] if text else []
        
    except Exception as e:
        print(f"[OCR] Error: {str(e)}")
        return []

