# 📊 Database Integration - Complete Guide

## ✅ What's Setup

Your OCR app now automatically **saves all results to SQLite database**!

---

## 🗄️ Database Structure

**Database File:** `ocr_results.db` (auto-created in ocr_web_app folder)

**Table:** `ocr_results` with these columns:
- `id` - Unique result ID
- `filename` - Original file name (e.g., "document.pdf")
- `file_type` - Type: "pdf", "image", or "csv"
- `extracted_text` - Full extracted text
- `pages` - Number of pages processed
- `timestamp` - When it was processed
- `status` - "success" or "error"
- `error_message` - Error details if any

---

## 🚀 How It Works

### **Automatic Saving**

When you upload and process files:

1. File is processed (PDF/Image → extract text)
2. **Automatically saved to database** ✅
3. Also available for CSV/PDF download
4. **You can query/export anytime!**

Example:
```
Upload PDF → Process → Text Extracted → SAVED TO DB ✅
```

---

## 📡 API Routes

### **1️⃣ Get All Results**
```
GET /api/database/all
```
Returns all OCR results from database as JSON

**Response:**
```json
{
  "success": true,
  "total": 5,
  "results": [
    {
      "id": 1,
      "filename": "document.pdf",
      "file_type": "pdf",
      "extracted_text": "...",
      "pages": 3,
      "timestamp": "2026-03-29 14:30:00",
      "status": "success"
    }
  ]
}
```

---

### **2️⃣ Get Statistics**
```
GET /api/database/stats
```
Get counts of results by type

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total_results": 10,
    "by_type": {"pdf": 5, "image": 3, "csv": 2},
    "successful": 9,
    "failed": 1
  }
}
```

---

### **3️⃣ Get Specific Result**
```
GET /api/database/result/<id>
```
Get details of specific result by ID

Example: `/api/database/result/1`

---

### **4️⃣ Export All as Excel**
```
GET /api/database/export
```
Download **all database results** as `.xlsx` file!

Perfect for analysis, reports, archiving.

---

## 💻 Using from Terminal/Python

### **View All Results**
```powershell
python -c "from src.database import get_all_results; print(get_all_results())"
```

### **Get Statistics**
```powershell
python -c "from src.database import get_statistics; print(get_statistics())"
```

### **Get Specific Result**
```powershell
python -c "from src.database import get_result_by_id; print(get_result_by_id(1))"
```

### **Delete a Result**
```powershell
python -c "from src.database import delete_result; print(delete_result(5))"
```

### **Clear All (⚠️ Use with caution!)**
```powershell
python -c "from src.database import clear_all_results; clear_all_results()"
```

---

## 📊 Example Workflow

### **Step 1: Upload & Process**
- Upload PDF/Image in browser
- Click "PROCESS FILES"
- → **Automatically saved to database!**

### **Step 2: View Results**
Open in browser or via API:
```
http://localhost:5000/api/database/all
```

### **Step 3: Export**
```
http://localhost:5000/api/database/export
```
→ Downloads `ocr_database_20260329_143000.xlsx`

### **Step 4: Analyze**
- Open Excel file
- Analyze all extracted text
- Sort, filter, create reports

---

## 🔍 Database File Locations

**Main database:**
```
C:\Users\cw\Desktop\opencv\ocr_web_app\ocr_results.db
```

**Python module:**
```
C:\Users\cw\Desktop\opencv\ocr_web_app\src\database.py
```

---

## 📈 Advanced Usage

### **Query from Python Script**

```python
from src.database import Session, OCRResult

session = Session()

# Get all PDFs
pdfs = session.query(OCRResult).filter(
    OCRResult.file_type == 'pdf'
).all()

# Get all successful results
successes = session.query(OCRResult).filter(
    OCRResult.status == 'success'
).all()

# Get last 10 results
recent = session.query(OCRResult).order_by(
    OCRResult.id.desc()
).limit(10).all()

session.close()
```

---

## ✨ Benefits

✅ **Permanent Storage** - Results never lost  
✅ **Easy Retrieval** - Query anytime  
✅ **Export Formats** - Excel, JSON, PDF  
✅ **Statistics** - Track processing history  
✅ **Error Tracking** - Know which files failed  
✅ **Scalable** - Grows with your data  

---

## 🎯 Quick Access

**Browser URLs:**
- View all: `http://localhost:5000/api/database/all`
- Statistics: `http://localhost:5000/api/database/stats`
- Export: `http://localhost:5000/api/database/export`
- View one: `http://localhost:5000/api/database/result/1`

---

## 🐛 Troubleshooting

**Q: Database file not created?**  
A: Check if app is running. Database auto-creates on first run.

**Q: Can't see old results?**  
A: Restart app - it loads existing database automatically.

**Q: Export not working?**  
A: Install openpyxl: `pip install openpyxl`

**Q: Want to start fresh?**  
A: Delete `ocr_results.db` and restart app.

---

**That's it! Your results are now safe in the database.** 🎉
