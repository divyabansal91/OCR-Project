# OCR Web Application

**A complete web application for intelligent document processing using OCR, Python, Flask, and Machine Learning.**

## 📋 Overview

This project converts PDFs, images, and CSV files into structured text data using Tesseract OCR and advanced image preprocessing techniques. Perfect for document digitization, data extraction, and workflow automation.

## ✨ Features

- ✅ **Multi-format Support**: PDFs, JPG, PNG, BMP, TIFF, CSV
- ✅ **Multi-page PDF Processing**: Automatic page extraction and processing
- ✅ **Advanced Image Preprocessing**: Adaptive thresholding, denoising, morphological operations
- ✅ **High-accuracy OCR**: Tesseract OCR engine integration
- ✅ **Batch Processing**: Upload and process multiple files simultaneously
- ✅ **Results Export**: Download results as CSV or PDF
- ✅ **REST API**: Ready for integration with other applications
- ✅ **Intelligent Fallback**: PyMuPDF fallback when Poppler unavailable
- ✅ **Real-time Preview**: Web interface with live results

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Flask 3.0.3 |
| **PDF Processing** | PyMuPDF 1.27.2, pdf2image 1.17.0 |
| **Image Processing** | OpenCV 4.13.0 |
| **OCR Engine** | Tesseract OCR |
| **Text Extraction** | pytesseract 0.3.13 |
| **Data Processing** | Pandas 2.0+, SQLAlchemy 2.0+ |
| **Frontend** | HTML5, CSS3, JavaScript |

## 📁 Project Structure

```
ocr_web_app/
├── app.py                          # Main Flask application
├── main.py                        # Entry point
├── requirements.txt               # Python dependencies
├── requirements_updated.txt       # Updated dependencies
├── README.md                      # Project documentation
├── QUICK_START.md                # Quick start guide
├── SETUP_GUIDE.md                # Setup instructions
├── PDF_FIX_GUIDE.md              # PDF fix guide
├── POPPLER_IMPLEMENTATION.md     # Poppler setup guide
├── POSTMAN_GUIDE.md              # API testing guide
├── DATABASE_GUIDE.md             # Database guide
├── ML_INTEGRATION_GUIDE.md       # ML integration guide
│
├── src/
│   ├── __init__.py
│   ├── ocr_engine.py             # Tesseract OCR integration
│   ├── pdf_to_image.py           # PDF conversion with fallback
│   ├── preprocess.py             # Image preprocessing
│   ├── ml_models.py              # ML model integration
│   └── database.py               # Database operations
│
├── templates/
│   └── index.html                # Web interface
│
├── static/
│   ├── style.css                 # Styling
│   └── script.js                 # Frontend logic
│
├── data/                         # Storage for uploads & results
│   └── *.csv                     # Sample datasets
│
├── env_ocr/                      # Python virtual environment
│
├── scripts/
│   ├── install_poppler.py        # Auto-install Poppler
│   ├── auto_setup_poppler.py     # Non-interactive setup
│   ├── test_pdf_setup.py         # PDF setup verification
│   ├── test_pdf_processing.py    # PDF processing test
│   └── setup_poppler.py          # Manual Poppler setup
│
├── .gitignore                    # Git ignore rules
└── OCR_Web_App_Postman_Collection.json  # Postman API collection
```

## 🚀 Quick Start

### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/ocr-web-app.git
cd ocr-web-app
```

### 2. **Setup Virtual Environment**
```bash
# Create virtual environment
python -m venv env_ocr

# Activate it
# Windows
.\env_ocr\Scripts\Activate

# Mac/Linux
source env_ocr/bin/activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements_updated.txt
```

### 4. **Install Tesseract OCR**

**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install to: `C:\Program Files\Tesseract-OCR`

**Mac:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### 5. **[OPTIONAL] Install Poppler for Better Quality**
```bash
# Run auto-installer
python auto_setup_poppler.py
```

### 6. **Run the Application**
```bash
python app.py
```

### 7. **Open in Browser**
```
http://localhost:5000
```

## 📝 API Usage

### Upload Files
```bash
curl -X POST http://localhost:5000/upload \
  -F "files[]=@document.pdf"
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "filename": "document.pdf",
      "text": "Extracted text...",
      "pages": 4
    }
  ],
  "session_id": "20260408_150552",
  "total_pages": 4
}
```

### Download Results
```bash
# As CSV
curl http://localhost:5000/download/csv/20260408_150552 -o results.csv

# As PDF
curl http://localhost:5000/download/pdf/20260408_150552 -o results.pdf
```

## 🧪 Testing

### Test PDF Processing
```bash
python test_pdf_processing.py
```

### Test with Postman
1. Import `OCR_Web_App_Postman_Collection.json` into Postman
2. Use provided requests to test all endpoints
3. Upload test files from `data/` folder

## 🔍 How It Works

```
Input File (PDF/Image/CSV)
        ↓
┌─────────────────────────────┐
│ Try Poppler (200 DPI)       │ ← Best quality
└─────────────────────────────┘
        ↓ (Fallback)
┌─────────────────────────────┐
│ Use PyMuPDF (150 DPI)       │ ← Always available
└─────────────────────────────┘
        ↓
┌─────────────────────────────┐
│ Image Preprocessing         │
│ • Grayscale conversion      │
│ • Adaptive thresholding     │
│ • Denoising                 │
│ • Morphological ops         │
└─────────────────────────────┘
        ↓
┌─────────────────────────────┐
│ Tesseract OCR               │
│ Extract text from image     │
└─────────────────────────────┘
        ↓
┌─────────────────────────────┐
│ Export Results              │
│ • CSV format                │
│ • PDF format                │
│ • JSON format               │
└─────────────────────────────┘
        ↓
Output (Extracted Text Data)
```

## 📊 Performance

| Operation | Time | Details |
|-----------|------|---------|
| Single page | ~2-3s | Image preprocessing + OCR |
| 4-page PDF | ~8-12s | Total processing time |
| 10-page PDF | ~20-30s | Batch processing |
| CSV export | <1s | Per document |

## 🎓 Learning Outcomes

Through building this project, I learned:

✓ **PDF Processing** - PyMuPDF, pdf2image, multi-page handling  
✓ **Image Preprocessing** - OpenCV, adaptive thresholding, denoising  
✓ **OCR Integration** - Tesseract engine, text extraction  
✓ **Flask Development** - REST APIs, file uploads, error handling  
✓ **Batch Processing** - Handling multiple files efficiently  
✓ **Fallback Mechanisms** - Graceful degradation when tools unavailable  
✓ **Testing** - Unit tests, integration tests with Postman  

## 🐛 Troubleshooting

### Tesseract Not Found
```bash
# Windows: Install from
https://github.com/UB-Mannheim/tesseract/wiki

# Update path in preprocess.py if needed
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### PDF Processing Fails
```bash
# Test setup
python test_pdf_processing.py

# Will use PyMuPDF fallback automatically
```

### Poor OCR Quality
- Ensure image is well-lit
- Use PDF with good resolution
- Check preprocessing settings in `src/preprocess.py`

## 📚 Documentation

- [Quick Start Guide](QUICK_START.md) - Get running in 5 minutes
- [Setup Guide](SETUP_GUIDE.md) - Detailed installation steps
- [PDF Fix Guide](PDF_FIX_GUIDE.md) - Troubleshoot PDF issues
- [Poppler Setup](POPPLER_IMPLEMENTATION.md) - Optional high-quality processing
- [API Testing](POSTMAN_GUIDE.md) - Test with Postman
- [Database Guide](DATABASE_GUIDE.md) - Database setup
- [ML Integration](ML_INTEGRATION_GUIDE.md) - Add ML features

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- LinkedIn: [@yourprofile](https://linkedin.com/in/yourprofile)
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) - OCR Engine
- [OpenCV](https://opencv.org/) - Image Processing
- [Flask](https://flask.palletsprojects.com/) - Web Framework
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF Processing
- [Poppler](https://poppler.freedesktop.org/) - PDF Rendering

## 📞 Support

Need help? 
- 📖 Check the documentation
- 🐛 Open an Issue
- 💬 Start a Discussion
- 📧 Contact me directly

---

**Made with ❤️ and lots of ☕**

Star this project if you found it useful! ⭐
