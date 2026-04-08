"""
Database Models and Management for OCR Results
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database configuration
DATABASE_URL = "sqlite:///ocr_results.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()

class OCRResult(Base):
    """
    Database model for storing OCR results
    """
    __tablename__ = "ocr_results"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, image, csv
    extracted_text = Column(Text, nullable=True)
    pages = Column(Integer, default=1)
    timestamp = Column(DateTime, default=datetime.now)
    status = Column(String(50), default="success")  # success, error
    error_message = Column(Text, nullable=True)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'file_type': self.file_type,
            'extracted_text': self.extracted_text,
            'pages': self.pages,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S") if self.timestamp else None,
            'status': self.status,
            'error_message': self.error_message
        }


def init_db():
    """Initialize database - create tables"""
    Base.metadata.create_all(engine)
    print("[DB] [OK] Database initialized successfully")


def save_result(filename, file_type, extracted_text, pages=1, error_message=None):
    """
    Save OCR result to database
    
    Args:
        filename: Source file name
        file_type: Type of file (pdf, image, csv)
        extracted_text: Extracted text content
        pages: Number of pages processed
        error_message: Error message if processing failed
    
    Returns:
        Result ID in database
    """
    try:
        session = Session()
        
        status = "error" if error_message else "success"
        
        result = OCRResult(
            filename=filename,
            file_type=file_type,
            extracted_text=extracted_text,
            pages=pages,
            status=status,
            error_message=error_message
        )
        
        session.add(result)
        session.commit()
        result_id = result.id
        session.close()
        
        print(f"[DB] [OK] Result saved with ID: {result_id}")
        return result_id
        
    except Exception as e:
        print(f"[DB] [ERROR] Error saving to database: {str(e)}")        
        return None


def get_all_results():
    """Get all OCR results from database"""
    try:
        session = Session()
        results = session.query(OCRResult).order_by(OCRResult.id.desc()).all()
        session.close()
        return [r.to_dict() for r in results]
    except Exception as e:
        print(f"[DB] [ERROR] Error retrieving results: {str(e)}")
        return []


def get_result_by_id(result_id):
    """Get specific result by ID"""
    try:
        session = Session()
        result = session.query(OCRResult).filter(OCRResult.id == result_id).first()
        session.close()
        return result.to_dict() if result else None
    except Exception as e:
        print(f"[DB] [ERROR] Error retrieving result: {str(e)}")
        return None


def get_results_by_type(file_type):
    """Get results filtered by file type"""
    try:
        session = Session()
        results = session.query(OCRResult).filter(
            OCRResult.file_type == file_type
        ).order_by(OCRResult.id.desc()).all()
        session.close()
        return [r.to_dict() for r in results]
    except Exception as e:
        print(f"[DB] [ERROR] Error filtering results: {str(e)}")
        return []


def delete_result(result_id):
    """Delete a result from database"""
    try:
        session = Session()
        result = session.query(OCRResult).filter(OCRResult.id == result_id).first()
        if result:
            session.delete(result)
            session.commit()
            session.close()
            print(f"[DB] [OK] Result {result_id} deleted")
            return True
        session.close()
        return False
    except Exception as e:
        print(f"[DB] [ERROR] Error deleting result: {str(e)}")
        return False


def clear_all_results():
    """Clear all results from database (use with caution!)"""
    try:
        session = Session()
        session.query(OCRResult).delete()
        session.commit()
        session.close()
        print("[DB] [OK] All results cleared")
        return True
    except Exception as e:
        print(f"[DB] [ERROR] Error clearing results: {str(e)}")
        return False


def get_statistics():
    """Get database statistics"""
    try:
        session = Session()
        total = session.query(OCRResult).count()
        by_type = {}
        for file_type in ['pdf', 'image', 'csv']:
            count = session.query(OCRResult).filter(
                OCRResult.file_type == file_type
            ).count()
            by_type[file_type] = count
        
        success = session.query(OCRResult).filter(
            OCRResult.status == 'success'
        ).count()
        
        session.close()
        
        return {
            'total_results': total,
            'by_type': by_type,
            'successful': success,
            'failed': total - success
        }
    except Exception as e:
        print(f"[DB] ✗ Error getting statistics: {str(e)}")
        return {}
