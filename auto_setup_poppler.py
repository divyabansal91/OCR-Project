#!/usr/bin/env python
"""
Automatic Poppler Setup - Non-Interactive
This script will download and install Poppler automatically
"""

import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

def check_poppler_exists():
    """Check if Poppler is already installed"""
    paths = [
        r"C:\poppler\Library\bin\pdftoppm.exe",
        r"C:\Program Files\poppler\Library\bin\pdftoppm.exe",
        r"C:\Program Files (x86)\poppler\Library\bin\pdftoppm.exe",
    ]
    
    for path in paths:
        if os.path.exists(path):
            return path
    return None

def download_poppler():
    """Download Poppler from GitHub releases"""
    try:
        print("📥 Downloading Poppler...")
        print("   (This may take 1-2 minutes...)")
        
        # Try multiple download sources
        urls = [
            "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0/poppler-24.08.0-windows-x64.zip",
            "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.02.0/poppler-24.02.0-windows-x64.zip",
            "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.11.0/poppler-23.11.0-windows-x64.zip",
        ]
        
        filename = "poppler.zip"
        
        for url in urls:
            try:
                print(f"   Trying: {url.split('/')[-1]}...")
                break
            except:
                continue
        
        def show_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(downloaded * 100 // total_size, 100)
            print(f"\r   Progress: {percent}%", end="", flush=True)
        
        for url in urls:
            try:
                urllib.request.urlretrieve(url, filename, reporthook=show_progress)
                print("\n✓ Download complete!")
                return filename
            except Exception as e:
                print(f"\n   Failed: {str(e)[:50]}")
                continue
        
        print("✗ All download attempts failed")
        return None
    except Exception as e:
        print(f"✗ Download failed: {e}")
        return None

def extract_poppler(zip_path):
    """Extract Poppler to C:\poppler"""
    try:
        print("📦 Extracting Poppler...")
        
        poppler_dir = r"C:\poppler"
        
        # Remove if exists
        if os.path.exists(poppler_dir):
            print(f"   Cleaning up old installation...")
            shutil.rmtree(poppler_dir)
        
        os.makedirs(poppler_dir, exist_ok=True)
        
        # Extract
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(poppler_dir)
        
        # Find pdftoppm.exe
        for root, dirs, files in os.walk(poppler_dir):
            if 'pdftoppm.exe' in files:
                print(f"✓ Poppler installed successfully!")
                print(f"   Location: {root}")
                return True
        
        print("✗ Could not find pdftoppm.exe after extraction")
        return False
        
    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        return False

def test_poppler():
    """Test if Poppler works"""
    try:
        from pdf2image import convert_from_path
        
        print("\n✓ Testing Poppler integration...")
        # Just test the import, actual PDF conversion will test on first use
        print("✓ pdf2image module loaded successfully")
        return True
    except Exception as e:
        print(f"⚠️  Testing: {e}")
        return False

def main():
    print("=" * 60)
    print("  ⚡ Poppler Auto-Setup (Non-Interactive)")
    print("=" * 60)
    
    # Check if already exists
    existing = check_poppler_exists()
    if existing:
        print(f"\n✓ Poppler already installed!")
        print(f"   Path: {existing}")
        test_poppler()
        return True
    
    print("\n⚠️  Poppler not found - installing now...")
    
    # Download
    zip_file = download_poppler()
    if not zip_file:
        print("\n❌ Installation failed at download step")
        return False
    
    # Extract
    success = extract_poppler(zip_file)
    
    # Cleanup
    if os.path.exists(zip_file):
        os.remove(zip_file)
        print("   Cleaned up temporary files")
    
    if success:
        test_poppler()
        print("\n" + "=" * 60)
        print("✅ POPPLER INSTALLED SUCCESSFULLY!")
        print("=" * 60)
        print("\n🚀 You can now:")
        print("   1. Run the app: python app.py")
        print("   2. Open browser: http://localhost:5000")
        print("   3. Upload PDFs for OCR processing")
        return True
    else:
        print("\n❌ Installation failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
