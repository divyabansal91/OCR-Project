#!/usr/bin/env powershell
# Quick Setup & Run Script for OCR Web App (PowerShell)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   OCR Web App - Quick Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\env_ocr\Scripts\Activate.ps1

# Check Poppler
Write-Host "`nChecking Poppler installation..." -ForegroundColor Yellow
$poppler_paths = @(
    "C:\poppler\Library\bin\pdftoppm.exe",
    "C:\Program Files\poppler\Library\bin\pdftoppm.exe",
    "C:\Program Files (x86)\poppler\Library\bin\pdftoppm.exe"
)

$poppler_found = $false
foreach ($path in $poppler_paths) {
    if (Test-Path $path) {
        Write-Host "✓ Poppler found at: $(Split-Path $path -Parent)" -ForegroundColor Green
        $poppler_found = $true
        break
    }
}

if (-not $poppler_found) {
    Write-Host "⚠️  Poppler not found!" -ForegroundColor Red
    Write-Host "Installing Poppler..." -ForegroundColor Yellow
    
    python install_poppler.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n❌ Poppler installation failed." -ForegroundColor Red
        Write-Host "Please install manually from:" -ForegroundColor Yellow
        Write-Host "https://github.com/oschwartz10612/poppler-windows/releases/`n" -ForegroundColor Yellow
        exit 1
    }
}

# Check Tesseract
Write-Host "`nChecking Tesseract-OCR installation..." -ForegroundColor Yellow
if (Test-Path "C:\Program Files\Tesseract-OCR\tesseract.exe") {
    Write-Host "✓ Tesseract-OCR found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Tesseract-OCR not found!" -ForegroundColor Yellow
    Write-Host "Download from: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Yellow
    Write-Host "Install to: C:\Program Files\Tesseract-OCR\`n" -ForegroundColor Yellow
}

# Start the app
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   Starting OCR Web App..." -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "🌐 Open browser: http://localhost:5000" -ForegroundColor Green
Write-Host "🔴 Press Ctrl+C to stop the server`n" -ForegroundColor Yellow

python app.py

Read-Host "Press Enter to exit"
