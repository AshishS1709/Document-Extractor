from typing import Dict, Optional, Union
import pytesseract
from PIL import Image
import io

class OCRAgent:
    """Handles OCR processing of documents."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the OCR agent with optional configuration."""
        self.config = config or {}
        
    def process_document(self, document: Union[bytes, str, Image.Image]) -> Dict:
        """
        Process a document and extract text using OCR.
        
        Args:
            document: Can be a file path (str), bytes, or PIL Image
            
        Returns:
            Dict containing extracted text and metadata
        """
        try:
            # Convert input to PIL Image if it's not already
            if isinstance(document, bytes):
                img = Image.open(io.BytesIO(document))
            elif isinstance(document, str):
                img = Image.open(document)
            else:
                img = document
                
            # Convert to grayscale for better OCR results
            if img.mode != 'L':
                img = img.convert('L')
                
            # Perform OCR
            text = pytesseract.image_to_string(img, **self.config.get('tesseract', {}))
            
            return {
                'status': 'success',
                'text': text,
                'metadata': {
                    'pages': 1,  # Default, can be updated for multi-page docs
                    'language': self.config.get('language', 'eng'),
                    'confidence': 0.0  # Can be updated with actual confidence
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'text': ''
            }
