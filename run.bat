@echo off
REM Quick Setup & Run Script for OCR Web App

echo.
echo ========================================
echo   OCR Web App - Quick Setup
echo ========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call env_ocr\Scripts\activate.bat

REM Check if Poppler is installed
echo.
echo Checking Poppler installation...
if exist "C:\poppler\Library\bin\pdftoppm.exe" (
    echo ✓ Poppler found at C:\poppler\
) else if exist "C:\Program Files\poppler\Library\bin\pdftoppm.exe" (
    echo ✓ Poppler found at C:\Program Files\poppler\
) else (
    echo.
    echo ⚠️  Poppler not found!
    echo Installing Poppler...
    python install_poppler.py
    if errorlevel 1 (
        echo.
        echo ❌ Poppler installation failed.
        echo Please install manually from:
        echo https://github.com/oschwartz10612/poppler-windows/releases/
        echo.
        pause
        exit /b 1
    )
)

REM Check Tesseract
echo.
echo Checking Tesseract-OCR installation...
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo ✓ Tesseract-OCR found
) else (
    echo ⚠️  Tesseract-OCR not found!
    echo Download from: https://github.com/UB-Mannheim/tesseract/wiki
    echo Install to: C:\Program Files\Tesseract-OCR\
)

REM Start the app
echo.
echo ========================================
echo   Starting OCR Web App...
echo ========================================
echo.
echo 🌐 Open browser: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
