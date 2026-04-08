#!/usr/bin/env python
"""
Automatic Poppler Installer for Windows
This script will download and install Poppler automatically
"""

import os
import sys
import subprocess
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
        import urllib.request
        print("📥 Downloading Poppler...")
        print("   (This may take a minute...)")
        
        # Using a direct download link - latest stable version
        # Try multiple mirrors if GitHub fails
        urls = [
            "https://github.com/oschwartz10612/poppler-windows/releases/download/v25.01.0/poppler-25.01.0-windows-x64.zip",
            "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0/poppler-24.08.0-windows-x64.zip",
        ]
        filename = "poppler.zip"
        
        for url in urls:
            try:
                urllib.request.urlretrieve(url, filename)
                print("✓ Download complete!")
                return filename
            except:
                continue
        
        raise Exception("All mirror URLs failed")
    except Exception as e:
        print(f"✗ Download failed: {e}")
        return None

def extract_poppler(zip_path):
    """Extract Poppler to C:\poppler"""
    try:
        print("📦 Extracting Poppler...")
        
        # Create poppler directory
        poppler_dir = r"C:\poppler"
        os.makedirs(poppler_dir, exist_ok=True)
        
        # Extract to C:\poppler
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(poppler_dir)
        
        # Find the actual poppler folder (might be nested)
        for root, dirs, files in os.walk(poppler_dir):
            if 'pdftoppm.exe' in files:
                print(f"✓ Poppler installed at: {root}")
                return True
        
        print("✗ Could not find pdftoppm.exe after extraction")
        return False
        
    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        return False

def main():
    print("=" * 60)
    print("  ⚡ Poppler Auto-Installer")
    print("=" * 60)
    
    # Check if Poppler already exists
    existing = check_poppler_exists()
    if existing:
        print(f"\n✓ Poppler already installed at:\n   {existing}")
        return True
    
    print("\n⚠️  Poppler not found!")
    print("    This is required for PDF processing.")
    
    # Ask user to continue
    response = input("\nDo you want to auto-install Poppler? (yes/no): ").strip().lower()
    if response != 'yes' and response != 'y':
        print("Installation cancelled.")
        return False
    
    # Download
    zip_file = download_poppler()
    if not zip_file:
        print("\n❌ Could not download Poppler")
        print("   Please download manually from:")
        print("   https://github.com/oschwartz10612/poppler-windows/releases/")
        return False
    
    # Extract
    if not extract_poppler(zip_file):
        print("❌ Could not extract Poppler")
        return False
    
    # Cleanup zip
    try:
        os.remove(zip_file)
    except:
        pass
    
    # Verify installation
    if check_poppler_exists():
        print("\n" + "=" * 60)
        print("  ✓ INSTALLATION COMPLETE!")
        print("=" * 60)
        print("\nPoppler has been installed successfully.")
        print("You can now process PDFs! 🎉")
        return True
    else:
        print("\n❌ Installation verification failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
