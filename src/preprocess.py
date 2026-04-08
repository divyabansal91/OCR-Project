import cv2
import os

def preprocess_image(image_path):
    """
    Preprocess image for better OCR results
    """
    try:
        # Read image
        img = cv2.imread(image_path)
        
        if img is None:
            raise Exception(f"Could not read image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Noise removal using bilateral filter
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Gaussian Blur for smoothing
        blur = cv2.GaussianBlur(denoised, (5, 5), 0)
        
        # Thresholding - using adaptive threshold for better results
        # This handles varying lighting conditions better than simple threshold
        thresh = cv2.adaptiveThreshold(
            blur, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 
            11, 2
        )
        
        # Morphological operations to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Save processed image
        processed_path = image_path.replace(".", "_processed.")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(processed_path) or ".", exist_ok=True)
        
        cv2.imwrite(processed_path, morph)
        
        return processed_path
        
    except Exception as e:
        print(f"[PREPROCESS] Error processing {image_path}: {str(e)}")
        # Return original path if processing fails
        return image_path