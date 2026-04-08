# =====================================================
# AI OCR Scanner - PowerShell Quick Start
# Run this file in PowerShell to start the app
# =====================================================

Write-Host ""
Write-Host "========================================"
Write-Host "  AI OCR Scanner - Starting..."
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to app directory
Set-Location "C:\Users\cw\Desktop\opencv\ocr_web_app"

# Activate virtual environment
Write-Host "[*] Activating virtual environment..." -ForegroundColor Yellow
& .\env_ocr\Scripts\Activate.ps1

# Show status
Write-Host ""
Write-Host "[✓] Virtual environment activated!" -ForegroundColor Green
Write-Host ""
Write-Host "[*] Starting Flask app..." -ForegroundColor Yellow
Write-Host ""

# Start the app
python app.py

# Pause if we exit
Write-Host ""
Write-Host "App stopped. Press any key to close..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
