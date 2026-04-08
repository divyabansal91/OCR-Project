# 📄 PDF Scanning - Troubleshooting Guide

## समस्या: PDF स्कैन नहीं हो रहा है (PDF Not Scanning)

### जड़ का कारण (Root Cause)
PDF को images में convert करने के लिए **Poppler** tool चाहिए। अगर यह installed नहीं है तो PDF काम नहीं करेगा।

---

## ✅ Solution: Poppler Install करें

### Step 1: Poppler Download करें
1. यहाँ जाएं: https://github.com/oschwartz10612/poppler-windows/releases/
2. सबसे नया **Release** download करें (e.g., `poppler-24.02.0-windows-x64.zip`)

### Step 2: Extract करें
```
C:\poppler\
     ├── Library\
     │   └── bin\
     │       ├── pdftoppm.exe
     │       ├── pdftotext.exe
     │       └── ... (अन्य files)
     └── ... (अन्य folders)
```

### Step 3: Path Set करें
तीन जगह में से कोई भी काम करेगा:
- `C:\poppler\Library\bin`
- `C:\Program Files\poppler\Library\bin`
- `C:\Program Files (x86)\poppler\Library\bin`

---

## 🧪 Poppler सही से installed है या नहीं check करें

### Virtual Environment में जाएं:
```powershell
.\env_ocr\Scripts\Activate.ps1
```

### Test Script चलाएं:
```powershell
python test_pdf_setup.py
```

### Expected Output:
```
✓ OpenCV: 4.13.0.92
✓ pdf2image: 1.17.0
✓ pytesseract: installed
✓ Poppler found at: C:\poppler\Library\bin
✓ Tesseract found at: C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

## 🔧 Tesseract भी Check करें

Tesseract-OCR **OCR** के लिए चाहिए (text निकालने के लिए)।

### Download करें:
https://github.com/UB-Mannheim/tesseract/wiki

### Install करें:
```
C:\Program Files\Tesseract-OCR\
```

### Path Update करें (अगर जरूरत हो):
[src/ocr_engine.py](src/ocr_engine.py) में यह line update करें:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## 🎯 PDF Scanning Test करें

1. App को start करें:
```powershell
python app.py
```

2. Browser में जाएं: `http://localhost:5000`

3. एक PDF upload करें

4. "Process Files" button दबाएं

5. देखें कि text extract हो रहा है या error आ रहा है

---

## 🚨 Common Errors

### Error: "Poppler not found"
**समाधान:**
- Poppler को correct path में extract करें
- Path को check करें: `C:\poppler\Library\bin\pdftoppm.exe` exist करना चाहिए

### Error: "ModuleNotFoundError: No module named 'pdf2image'"
**समाधान:**
```powershell
pip install pdf2image
```

### Error: "Tesseract not found"
**समाधान:**
- Tesseract-OCR install करें
- [src/ocr_engine.py](src/ocr_engine.py) में exact path enter करें

### PDF converts हो रहा है लेकिन text नहीं निकल रहा
**संभावित कारण:**
- PDF scanned image है (not searchable)
- OCR accuracy issue

**समाधान:**
- Better quality PDF upload करें
- Image को cleaner बनाने के लिए preprocessing improve करें

---

## 📝 अपनी PDF path manually set करें

अगर आपकी Poppler default path में नहीं है, तो [src/pdf_to_image.py](src/pdf_to_image.py) में यह add करें:

```python
poppler_path = r"C:\your\custom\poppler\path\Library\bin"

images = convert_from_path(
    pdf_path,
    poppler_path=poppler_path
)
```

---

## ✨ सही तरीका (Step by Step)

```
1. Poppler डाउनलोड करें
   ↓
2. C:\poppler\ में extract करें
   ↓
3. test_pdf_setup.py चलाएं
   ↓
4. सभी checks ✓ आएं
   ↓
5. App को restart करें
   ↓
6. PDF upload करें और test करें
```

---

## 💡 Additional Tips

- **Larger PDFs**: बहुत बड़ी PDFs slow हो सकती हैं
- **Scanned PDFs**: अगर manually scanned हैं, तो Tesseract quality affect होती है
- **Memory**: Multiple large PDFs एक साथ upload करने से memory issue हो सकता है

---

अगर अभी भी issue है तो `test_pdf_setup.py` चलाकर exact error message share करें।

Happy Scanning! 🚀
