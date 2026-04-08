# 🚀 AI OCR Scanner - Quick Start Guide

## ⚡ Fastest Way to Start

### **Windows Users - Just Double-Click!**

1. **Open File Explorer**
2. Navigate to: `C:\Users\cw\Desktop\opencv\ocr_web_app\`
3. **Double-click:** `START_APP.bat`
4. Wait for the terminal to show:
   ```
   Running on http://127.0.0.1:5000
   ```
5. **Open browser:** `http://localhost:5000`

That's it! 🎉

---

## 📋 What These Files Do

| File | Purpose |
|------|---------|
| `START_APP.bat` | ⭐ Click this to start the app |
| `OPEN_BROWSER.bat` | Quick shortcut to browser |
| `app.py` | Main Flask application |

---

## 🔧 Manual Start (if batch doesn't work)

Open PowerShell in the `ocr_web_app` folder and paste:

```powershell
.\env_ocr\Scripts\Activate.ps1; python app.py
```

---

## 🌐 Access the App

Once running, open your browser and go to:

```
http://localhost:5000
```

---

## 📄 Supported Formats

✅ **Images:** JPG, PNG, BMP, TIFF
✅ **PDFs:** All PDF types (scanned & text-based)
✅ **CSV:** Data extraction & preview

---

## ⬇️ Download Options

After processing, download results as:
- 📊 **CSV File**
- 📄 **PDF Report**

---

## 🛑 Stop the App

Press **CTRL + C** in the terminal

---

## 📧 Troubleshooting

**Port 5000 already in use?**
```powershell
# Find process using port 5000
Get-NetTCPConnection -LocalPort 5000

# Kill it if needed
Stop-Process -Id <PID> -Force
```

**Tesseract not installed?**
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Install to: `C:\Program Files\Tesseract-OCR\`

**Poppler for better PDF quality?**
- Run: `python setup_poppler.py`
- Or download manually from: https://github.com/oschwartz10612/poppler-windows/releases/

---

## 🎯 Next Steps

1. ✅ Start the app
2. 📤 Upload your files
3. ⚙️ Click "PROCESS FILES"
4. 📊 Download results

**Enjoy!** 🚀
