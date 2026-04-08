@echo off
echo ========================================
echo  OCR Web App - Setup Script
echo ========================================
echo.
echo Creating virtual environment...
python -m venv env_ocr

echo.
echo Activating virtual environment...
call env_ocr\Scripts\activate.bat

echo.
echo Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Installing requirements...
pip install -r requirements.txt

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo To activate the environment in the future, run:
echo   env_ocr\Scripts\activate.bat
echo.
echo To run the app:
echo   python app.py
echo.
pause
