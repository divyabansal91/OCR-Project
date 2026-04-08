#!/usr/bin/env python
"""
PDF Troubleshooting Script
Run this to check if PDF processing setup is correct
"""

import os
import sys

print("=" * 60)
print("OCR Web App - PDF Setup Check")
print("=" * 60)

# Check Python version
print(f"\n✓ Python Version: {sys.version}")

# Check cv2 (OpenCV)
try:
    import cv2
    print(f"✓ OpenCV: {cv2.__version__}")
except ImportError:
    print("✗ OpenCV not installed!")
    sys.exit(1)

# Check pdf2image
try:
    import pdf2image
    print(f"✓ pdf2image: {pdf2image.__version__}")
except ImportError:
    print("✗ pdf2image not installed!")
    sys.exit(1)

# Check pytesseract
try:
    import pytesseract
    print("✓ pytesseract: installed")
except ImportError:
    print("✗ pytesseract not installed!")
    sys.exit(1)

# Check for Tesseract installation
print("\n" + "=" * 60)
print("Checking External Tools...")
print("=" * 60)

# Check Tesseract OCR
tesseract_paths = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]

tesseract_found = False
for path in tesseract_paths:
    if os.path.exists(path):
        print(f"✓ Tesseract found at: {path}")
        tesseract_found = True
        break

if not tesseract_found:
    print("✗ Tesseract-OCR not found!")
    print("   Download from: https://github.com/UB-Mannheim/tesseract/wiki")
    print("   Install to: C:\\Program Files\\Tesseract-OCR\\")

# Check Poppler
poppler_paths = [
    r"C:\poppler\Library\bin",
    r"C:\Program Files\poppler\Library\bin",
    r"C:\Program Files (x86)\poppler\Library\bin",
]

poppler_found = False
for path in poppler_paths:
    if os.path.exists(path):
        print(f"✓ Poppler found at: {path}")
        poppler_found = True
        break

if not poppler_found:
    print("✗ Poppler not found!")
    print("   Download from: https://github.com/oschwartz10612/poppler-windows/releases/")
    print("   Extract to: C:\\poppler\\")

# Test PDF conversion
print("\n" + "=" * 60)
print("Testing PDF Conversion...")
print("=" * 60)

if poppler_found and os.path.exists("data"):
    # Check if there's a test PDF
    pdf_files = [f for f in os.listdir("data") if f.lower().endswith(".pdf")]
    if pdf_files:
        test_pdf = os.path.join("data", pdf_files[0])
        print(f"Found test PDF: {pdf_files[0]}")
        
        try:
            from pdf2image import convert_from_path
            poppler_path = None
            for path in poppler_paths:
                if os.path.exists(path):
                    poppler_path = path
                    break
            
            images = convert_from_path(test_pdf, poppler_path=poppler_path)
            print(f"✓ Successfully converted PDF to {len(images)} page(s)")
        except Exception as e:
            print(f"✗ PDF conversion failed: {str(e)}")
    else:
        print("No PDF files found in data/ folder for testing")
else:
    print("Cannot test PDF conversion (Poppler not found or data folder missing)")

print("\n" + "=" * 60)
print("Setup Check Complete!")
print("=" * 60)
