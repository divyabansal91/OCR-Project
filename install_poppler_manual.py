#!/usr/bin/env python
"""
Alternative: Download Poppler from Xpdf or use system alternative
"""

import os
import sys
import subprocess
import zipfile
import urllib.request
from pathlib import Path

def check_poppler_exists():
    """Check if Poppler is already installed"""
    paths = [
        r"C:\poppler\Library\bin",
        r"C:\Program Files\poppler\Library\bin",
        r"C:\Program Files (x86)\poppler\Library\bin",
    ]
    
    for path in paths:
        dll_path = os.path.join(path, "pdftoppm.exe")
        if os.path.exists(dll_path):
            return path
    return None

def main():
    print("=" * 70)
    print("  📄 Poppler Installation Helper")
    print("=" * 70)
    
    # Check if already installed
    existing = check_poppler_exists()
    if existing:
        print(f"\n✅ Poppler found at: {existing}")
        return True
    
    print("\n❌ Poppler not found!")
    print("\n" + "=" * 70)
    print("MANUAL INSTALLATION STEPS:")
    print("=" * 70)
    print("""
1. Open this link in your browser:
   https://github.com/oschwartz10612/poppler-windows/releases

2. Download the LATEST version (e.g., poppler-XX.XX.X-windows-x64.zip)
   NOT the ones with -minimal in the name!

3. Extract the ZIP file to:
   C:\\poppler\\
   
   (So you should have: C:\\poppler\\Library\\bin\\pdftoppm.exe)

4. Once extracted, run setup_poppler.py again to verify!

5. Or simply restart the app and it will automatically detect Poppler!
    """)
    
    print("\n" + "=" * 70)
    print("NEED HELP?")
    print("=" * 70)
    print("""
If manual download fails, try these alternative approaches:

Option A: Use standalone binary
- Download: https://blog.alivate.com.au/poppler-windows/
- Or: https://anaconda.org/conda-forge/poppler (via Conda)

Option B: Install via Chocolatey (if installed)
  choco install poppler

Option C: Use Docker (advanced)
- Run PDF processing in Docker container with pre-installed Poppler
    """)
    
    # Ask for retry
    response = input("\nPress Enter after installing Poppler, or type 'skip' to continue anyway: ").strip().lower()
    
    if response != 'skip':
        if check_poppler_exists():
            print("✅ Poppler detected! Ready to use.")
            return True
    
    print("⚠️  Warning: PDF processing may fail without Poppler")
    return False

if __name__ == "__main__":
    main()
