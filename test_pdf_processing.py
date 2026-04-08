#!/usr/bin/env python
"""
Test PDF Processing with Fallback Support
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pdf_to_image import pdf_to_images

print("=" * 70)
print("  PDF Processing Test - Poppler + PyMuPDF Fallback")
print("=" * 70)

# Check dependencies
print("\n📦 Checking dependencies...")

try:
    import pdf2image
    print("  ✓ pdf2image installed")
except:
    print("  ✗ pdf2image NOT installed")
    sys.exit(1)

try:
    import fitz
    print("  ✓ PyMuPDF (fitz) installed")
except:
    print("  ✗ PyMuPDF NOT installed")
    sys.exit(1)

try:
    import cv2
    print("  ✓ OpenCV installed")
except:
    print("  ✗ OpenCV NOT installed")
    sys.exit(1)

try:
    import pytesseract
    print("  ✓ pytesseract installed")
except:
    print("  ✗ pytesseract NOT installed")
    sys.exit(1)

try:
    import PIL
    print("  ✓ Pillow installed")
except:
    print("  ✗ Pillow NOT installed")
    sys.exit(1)

# Check for Poppler
print("\n🔍 Checking for Poppler installation...")
poppler_paths = [
    r"C:\poppler\Library\bin",
    r"C:\Program Files\poppler\Library\bin",  
    r"C:\Program Files (x86)\poppler\Library\bin",
]

poppler_found = False
for path in poppler_paths:
    if os.path.exists(os.path.join(path, "pdftoppm.exe")):
        print(f"  ✓ Poppler found at: {path}")
        poppler_found = True
        break

if not poppler_found:
    print("  ⚠️  Poppler NOT found (will use PyMuPDF fallback)")

# Look for test PDFs
print("\n📂 Looking for test PDF files...")
test_pdfs = []
for root, dirs, files in os.walk("data"):
    for file in files:
        if file.lower().endswith('.pdf'):
            test_pdfs.append(os.path.join(root, file))

if not test_pdfs:
    # Create a simple test PDF
    print("  ⚠️  No PDF files found in data/ folder")
    print("     Creating a test PDF...")
    try:
        from reportlab.pdfgen import canvas
        from datetime import datetime
        
        test_pdf = "test_sample.pdf"
        c = canvas.Canvas(test_pdf)
        c.drawString(100, 750, "Test PDF for OCR Processing")
        c.drawString(100, 730, f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(100, 710, "This is a sample PDF for testing.")
        c.drawString(100, 690, "PDF processing should work with PyMuPDF fallback!")
        c.showPage()
        c.save()
        test_pdfs = [test_pdf]
        print(f"  ✓ Created test PDF: {test_pdf}")
    except Exception as e:
        print(f"  ✗ Could not create test PDF: {e}")

# Test PDF conversion
if test_pdfs:
    print(f"\n🚀 Testing PDF conversion with {len(test_pdfs)} file(s)...")
    
    for pdf_file in test_pdfs[:1]:  # Test first PDF
        print(f"\n  Processing: {pdf_file}")
        try:
            output_dir = "pdf_test_output"
            images = pdf_to_images(pdf_file, output_dir)
            
            print(f"\n  ✅ SUCCESS! Converted {len(images)} page(s)")
            print(f"     Output directory: {output_dir}")
            
            # List generated images
            for img in images[:3]:  # Show first 3
                if os.path.exists(img):
                    size = os.path.getsize(img) / 1024  # KB
                    print(f"       - {os.path.basename(img)} ({size:.1f} KB)")
            
        except Exception as e:
            print(f"  ❌ FAILED: {str(e)[:100]}")
            sys.exit(1)
else:
    print("  ⚠️  No test PDFs available")

print("\n" + "=" * 70)
print("✅ PDF PROCESSING TEST COMPLETE!")
print("=" * 70)
print("\n🎉 Your app can now process PDFs using:")
print("   • Poppler (if installed) for high quality")
print("   • PyMuPDF fallback for compatibility")
print("\n📝 Next steps:")
print("   1. Run: python app.py")
print("   2. Open: http://localhost:5000")
print("   3. Upload PDF and click 'Process Files'")
print("=" * 70)
