from pdf2image import convert_from_path
import os
import sys

def pdf_to_images(pdf_path, output_folder):
    """
    Convert PDF to images with automatic fallback
    Tries Poppler first (better quality), falls back to PyMuPDF if not found
    """
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # First, try Poppler (higher quality)
    images = try_poppler_conversion(pdf_path)
    
    if images is None:
        print("[PDF] Poppler not available, trying PyMuPDF fallback...")
        images = try_pymupdf_conversion(pdf_path)
    
    if images is None:
        raise Exception(
            "❌ PDF CONVERSION FAILED!\n\n"
            "Neither Poppler nor PyMuPDF could process the PDF.\n"
            "Please ensure the PDF file is valid and readable."
        )
    
    # Save images to files
    image_paths = save_images_to_disk(images, output_folder)
    
    print(f"[PDF] ✓ Conversion complete: {len(image_paths)} pages processed")
    return image_paths

def try_poppler_conversion(pdf_path):
    """Try to convert PDF using Poppler (higher quality)"""
    try:
        # List of possible Poppler paths (in order of preference)
        poppler_paths = [
            r"C:\poppler\Library\bin",
            r"C:\Program Files\poppler\Library\bin",  
            r"C:\Program Files (x86)\poppler\Library\bin",
            os.path.join(os.path.dirname(__file__), "..", "poppler", "Library", "bin"),
            None  # Try system PATH
        ]
        
        images = None
        
        # Try each Poppler path
        for poppler_path in poppler_paths:
            try:
                # Skip if path doesn't exist (except None which uses system PATH)
                if poppler_path is not None and not os.path.exists(poppler_path):
                    continue
                
                print(f"[PDF] Trying Poppler at: {poppler_path if poppler_path else 'System PATH'}")
                
                images = convert_from_path(
                    pdf_path,
                    poppler_path=poppler_path,
                    dpi=200  # Good quality for OCR
                )
                
                if images and len(images) > 0:
                    print(f"[PDF] ✓ Successfully converted using Poppler (200 DPI, high quality)")
                    return images
                    
            except Exception as e:
                print(f"[PDF] Poppler attempt failed: {str(e)[:60]}")
                continue
        
        return None
        
    except Exception as e:
        print(f"[PDF] Poppler conversion error: {str(e)[:60]}")
        return None

def try_pymupdf_conversion(pdf_path):
    """Fallback: Convert PDF using PyMuPDF (fitz)"""
    try:
        import fitz  # PyMuPDF
        
        print("[PDF] Using PyMuPDF for PDF conversion...")
        
        doc = fitz.open(pdf_path)
        images = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Render page to image (150 DPI for quality/speed balance)
            # Using zoom for better quality than direct rendering
            mat = fitz.Matrix(1.5, 1.5)  # 150% zoom for better quality
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            # Convert PyMuPDF pixmap to PIL Image for consistency
            from PIL import Image
            import numpy as np
            
            # Get image as RGB
            img_data = pix.tobytes("ppm")
            img = Image.open(__import__('io').BytesIO(img_data))
            
            images.append(img)
            print(f"[PDF] ✓ Rendered page {page_num + 1}")
        
        doc.close()
        
        if images:
            print(f"[PDF] ✓ Successfully converted using PyMuPDF ({len(images)} pages)")
            return images
        else:
            return None
            
    except ImportError:
        print("[PDF] ✗ PyMuPDF not installed (try: pip install PyMuPDF)")
        return None
    except Exception as e:
        print(f"[PDF] PyMuPDF conversion error: {str(e)[:60]}")
        return None

def save_images_to_disk(images, output_folder):
    """Save PIL images to disk"""
    image_paths = []
    from datetime import datetime
    
    for i, img in enumerate(images):
        # Use timestamp to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        img_path = os.path.join(output_folder, f"{timestamp}page_{i+1}.jpg")
        
        # Convert PIL image to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img.save(img_path, "JPEG", quality=95)
        image_paths.append(img_path)
        print(f"[PDF] ✓ Saved page {i+1}: {img_path}")
    
    return image_paths