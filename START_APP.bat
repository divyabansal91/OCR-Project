@echo off
REM =====================================================
REM  AI OCR Scanner - Quick Start
REM  Double-click this file to start the app!
REM =====================================================

cls
echo.
echo ========================================
echo   AI OCR Scanner - Starting...
echo ========================================
echo.

REM Navigate to the app directory
cd /d C:\Users\cw\Desktop\opencv\ocr_web_app

REM Activate virtual environment
call env_ocr\Scripts\activate.bat

REM Start the Flask app
echo.
echo [INFO] Starting Flask app...
echo [INFO] Open browser: http://localhost:5000
echo.
python app.py

REM Keep window open if there's an error
pause
