"""
Machine Learning Models for OCR Results Analysis
Includes: Sentiment Analysis, NER, Document Classification
"""

import warnings
warnings.filterwarnings('ignore')

# Lazy import transformers to avoid errors if not installed
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("[ML] [WARNING] Transformers not available - ML models disabled")

# Initialize models (lazy loading - load only when needed)
_sentiment_model = None
_ner_model = None
_classification_model = None

def get_sentiment_analyzer():
    """Get or initialize sentiment analysis model"""
    global _sentiment_model
    if not TRANSFORMERS_AVAILABLE:
        return None
    if _sentiment_model is None:
        print("[ML] Loading sentiment analysis model...")
        try:
            _sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        except Exception as e:
            print(f"[ML] Failed to load sentiment model: {str(e)}")
            return None
    return _sentiment_model

def get_ner_model():
    """Get or initialize NER model"""
    global _ner_model
    if not TRANSFORMERS_AVAILABLE:
        return None
    if _ner_model is None:
        print("[ML] Loading NER model...")
        try:
            _ner_model = pipeline("ner", aggregation_strategy="simple")
        except Exception as e:
            print(f"[ML] Failed to load NER model: {str(e)}")
            return None
    return _ner_model

def get_zero_shot_classifier():
    """Get or initialize zero-shot classification model"""
    global _classification_model
    if not TRANSFORMERS_AVAILABLE:
        return None
    if _classification_model is None:
        print("[ML] Loading classification model...")
        try:
            _classification_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        except Exception as e:
            print(f"[ML] Failed to load classification model: {str(e)}")
            return None
    return _classification_model

def analyze_sentiment(text):
    """
    Analyze sentiment of text
    Returns: {'label': 'POSITIVE'/'NEGATIVE', 'score': 0-1}
    """
    try:
        if not TRANSFORMERS_AVAILABLE:
            return None
        if not text or len(text.strip()) < 10:
            return None
        
        analyzer = get_sentiment_analyzer()
        if analyzer is None:
            return None
        result = analyzer(text[:512])  # Limit to 512 chars
        return {
            'sentiment': result[0]['label'],
            'confidence': round(result[0]['score'], 3)
        }
    except Exception as e:
        print(f"[ML] Sentiment error: {str(e)}")
        return None

def extract_named_entities(text):
    """
    Extract named entities (Person, Location, Organization, etc.)
    Returns: List of entities with types
    """
    try:
        if not TRANSFORMERS_AVAILABLE:
            return []
        if not text or len(text.strip()) < 10:
            return []
        
        ner = get_ner_model()
        if ner is None:
            return []
        entities = ner(text[:512])  # Limit text length
        
        # Format results
        formatted = []
        for entity in entities:
            formatted.append({
                'text': entity['word'],
                'type': entity['entity_group'],
                'confidence': round(entity['score'], 3)
            })
        
        return formatted
    except Exception as e:
        print(f"[ML] NER error: {str(e)}")
        return []

def classify_document(text, candidate_labels=None):
    """
    Classify document type
    Candidate labels: Invoice, Receipt, Bank Statement, Identity Card, Contract, etc.
    """
    try:
        if not TRANSFORMERS_AVAILABLE:
            return None
        if not text or len(text.strip()) < 20:
            return None
        
        if candidate_labels is None:
            candidate_labels = [
                "Invoice", "Receipt", "Bank Statement", 
                "Identity Card", "Passport", "Receipt",
                "Contract", "Report", "Letter", "Email"
            ]
        
        classifier = get_zero_shot_classifier()
        if classifier is None:
            return None
        result = classifier(text[:512], candidate_labels)
        
        return {
            'document_type': result['labels'][0],
            'confidence': round(result['scores'][0], 3),
            'scores': {label: round(score, 3) for label, score in zip(result['labels'], result['scores'])}
        }
    except Exception as e:
        print(f"[ML] Classification error: {str(e)}")
        return None

def analyze_full(text):
    """
    Full analysis: Sentiment + NER + Document Classification
    Returns: Complete analysis results
    """
    try:
        analysis = {
            'sentiment': analyze_sentiment(text),
            'entities': extract_named_entities(text),
            'document_type': classify_document(text)
        }
        return analysis
    except Exception as e:
        print(f"[ML] Full analysis error: {str(e)}")
        return {
            'sentiment': None,
            'entities': [],
            'document_type': None
        }

def get_summary(text, max_length=150):
    """
    Generate summary of text (if text is long)
    """
    try:
        if not TRANSFORMERS_AVAILABLE:
            return None
        if len(text) < 100:
            return text
        
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(text[:1024], max_length=max_length, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"[ML] Summarization error: {str(e)}")
        return None
