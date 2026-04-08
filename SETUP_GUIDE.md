# OCR Web App Setup & Run Guide

## ✅ Requirements (Python 3.13.5)

```
Flask==3.0.3
opencv-python==4.13.0.92
pdf2image==1.17.0
pytesseract==0.3.13
Pillow==11.1.0
reportlab==4.0.9
pandas>=2.0
```

## 🚀 Quick Start

### Option 1: Using Batch Script (Windows)
```cmd
setup.bat
```

### Option 2: Manual Setup (PowerShell)
```powershell
# Create virtual environment
python -m venv env_ocr

# Activate it
.\env_ocr\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Option 3: Manual Setup (CMD)
```cmd
# Create virtual environment
python -m venv env_ocr

# Activate it
env_ocr\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Running the Application

After installing dependencies, run:

```bash
python app.py
```

The app will be available at: **http://localhost:5000**

## 📋 Prerequisites

Make sure you have installed:
- **Python 3.13.5** (system environment)
- **Tesseract-OCR**: [Download](https://github.com/UB-Mannheim/tesseract/wiki)
  - Default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- **Poppler**: [Download](https://github.com/oschwartz10612/poppler-windows/releases/)
  - Default path: `C:\poppler\Library\bin`

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'X'"
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Issue: Tesseract not found
- Install Tesseract, or update path in `src/ocr_engine.py`

### Issue: Poppler not found
- Install Poppler, or update path in `src/pdf_to_image.py`

## 📁 Project Structure

```
ocr_web_app/
  ├── app.py                  # Main Flask application
  ├── requirements.txt        # Python dependencies
  ├── setup.bat              # Windows setup script
  ├── src/
  │   ├── ocr_engine.py     # Tesseract OCR integration
  │   ├── pdf_to_image.py   # PDF processing
  │   └── preprocess.py     # Image preprocessing
  ├── static/
  │   ├── style.css         # Modern UI styling
  │   └── script.js         # Frontend functionality
  └── templates/
      └── index.html        # Web interface
```

## ✨ Features

✅ Upload images (JPG, PNG, BMP, TIFF)
✅ Process PDFs with multiple pages
✅ Scan CSV files
✅ AI-powered OCR extraction
✅ Download results as CSV or PDF
✅ Beautiful, animated UI
✅ Full-screen responsive design
✅ Drag & drop file upload

---

**Happy OCR Scanning!** 🚀
