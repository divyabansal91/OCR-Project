from flask import Flask, render_template, request, jsonify, send_file
import os
import cv2
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch

from src.pdf_to_image import pdf_to_images
from src.preprocess import preprocess_image
from src.ocr_engine import extract_text

app = Flask(__name__)

UPLOAD_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store extracted text in session
extracted_results = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        files = request.files.getlist("files[]")
        
        if not files:
            return jsonify({"error": "No files selected"}), 400
        
        all_results = []
        
        for file in files:
            if not file or file.filename == '':
                continue
            
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            
            result = process_file(file_path, file.filename)
            if result:
                all_results.append(result)
        
        # Store results for download
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        extracted_results[session_id] = all_results
        
        return jsonify({
            "success": True,
            "results": all_results,
            "session_id": session_id,
            "total_pages": sum(r.get("pages", 1) for r in all_results)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_file(file_path, filename):
    """Process a single file and extract text"""
    extracted_text = ""
    pages = 0
    
    try:
        # PDF case
        if filename.lower().endswith(".pdf"):
            try:
                image_paths = pdf_to_images(file_path, UPLOAD_FOLDER)
                pages = len(image_paths)
                
                if pages == 0:
                    return {
                        "filename": filename,
                        "text": "Error: No pages found in PDF",
                        "pages": 0,
                        "error": True
                    }
                
                for idx, img_path in enumerate(image_paths):
                    try:
                        processed_path = preprocess_image(img_path)
                        img = cv2.imread(processed_path)
                        if img is None:
                            extracted_text += f"--- Page {idx + 1} ---\n[Error reading image]\n\n"
                            continue
                        text = extract_text(img)
                        extracted_text += f"--- Page {idx + 1} ---\n{text}\n\n"
                    except Exception as page_error:
                        extracted_text += f"--- Page {idx + 1} ---\n[Error: {str(page_error)}]\n\n"
                        continue
                
            except Exception as pdf_error:
                return {
                    "filename": filename,
                    "text": f"PDF Processing Error: {str(pdf_error)}",
                    "pages": 0,
                    "error": True
                }
        
        # CSV case
        elif filename.lower().endswith(".csv"):
            try:
                df = pd.read_csv(file_path)
                # Process first column or all text columns
                for col in df.columns:
                    if df[col].dtype == 'object':
                        for text in df[col].dropna():
                            extracted_text += process_image_from_text(str(text)) + "\n"
                pages = len(df)
            except Exception as csv_error:
                return {
                    "filename": filename,
                    "text": f"CSV Processing Error: {str(csv_error)}",
                    "pages": 0,
                    "error": True
                }
        
        # Image case
        else:
            try:
                processed_path = preprocess_image(file_path)
                img = cv2.imread(processed_path)
                if img is None:
                    return {
                        "filename": filename,
                        "text": "Error: Could not read image file",
                        "pages": 0,
                        "error": True
                    }
                extracted_text = extract_text(img)
                pages = 1
            except Exception as img_error:
                return {
                    "filename": filename,
                    "text": f"Image Processing Error: {str(img_error)}",
                    "pages": 0,
                    "error": True
                }
        
        if not extracted_text.strip():
            extracted_text = "[No text found in file]"
        
        return {
            "filename": filename,
            "text": extracted_text,
            "pages": pages
        }
    
    except Exception as e:
        return {
            "filename": filename,
            "text": f"Error processing file: {str(e)}",
            "pages": 0,
            "error": True
        }

def process_image_from_text(text):
    """Helper function to process text from CSV"""
    return text

@app.route("/download/<format>/<session_id>", methods=["GET"])
def download(format, session_id):
    """Download results in CSV or PDF format"""
    try:
        if session_id not in extracted_results:
            return jsonify({"error": "Session not found"}), 404
        
        results = extracted_results[session_id]
        
        if format == "csv":
            return download_csv(results)
        elif format == "pdf":
            return download_pdf(results)
        else:
            return jsonify({"error": "Invalid format"}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def download_csv(results):
    """Generate CSV file from results"""
    data = []
    for result in results:
        data.append({
            "filename": result["filename"],
            "extracted_text": result["text"],
            "pages": result["pages"]
        })
    
    df = pd.DataFrame(data)
    
    output = BytesIO()
    df.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)
    
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"ocr_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

def download_pdf(results):
    """Generate PDF file from results"""
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2c3e50',
        spaceAfter=30,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#3498db',
        spaceAfter=12,
        spaceBefore=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Title
    elements.append(Paragraph("OCR Extraction Results", title_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Results
    for result in results:
        elements.append(Paragraph(f"File: {result['filename']}", heading_style))
        elements.append(Paragraph(f"Pages: {result['pages']}", styles['Normal']))
        
        text_content = result['text'][:5000]  # Limit to first 5000 chars per PDF
        if len(result['text']) > 5000:
            text_content += "\n...(truncated)"
        
        elements.append(Paragraph(text_content.replace('\n', '<br/>'), body_style))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(PageBreak())
    
    doc.build(elements)
    output.seek(0)
    
    return send_file(
        output,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"ocr_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)