import pytest
import os
from book import GCEcoBook


class TestOCR:
    def setup_method(self):
        """Setup test fixtures"""
        self.book = GCEcoBook()
        self.test_image_path = "data/receipts/test_receipt.png"
    
    def test_preprocess_image_success(self):
        """Test successful image preprocessing"""
        if not os.path.exists(self.test_image_path):
            pytest.skip("Test image not found")
        
        preprocessed_path = self.book._preprocess_image(self.test_image_path)
        
        # Check that preprocessed file was created
        assert os.path.exists(preprocessed_path)
        assert preprocessed_path.endswith("_preprocessed.png")
        
        # Clean up
        os.remove(preprocessed_path)
    
    def test_preprocess_image_file_not_found(self):
        """Test preprocessing with non-existent file"""
        with pytest.raises(FileNotFoundError):
            self.book._preprocess_image("non_existent_file.png")
    
    def test_preprocess_image_unsupported_format(self):
        """Test preprocessing with unsupported format"""
        # Create a dummy file with unsupported extension
        dummy_file = "test_dummy.txt"
        with open(dummy_file, "w") as f:
            f.write("dummy content")
        
        try:
            with pytest.raises(ValueError, match="Unsupported image format"):
                self.book._preprocess_image(dummy_file)
        finally:
            if os.path.exists(dummy_file):
                os.remove(dummy_file)
    
    def test_extract_text_success(self):
        """Test successful text extraction"""
        if not os.path.exists(self.test_image_path):
            pytest.skip("Test image not found")
        
        text = self.book._extract_text_from_image(self.test_image_path)
        
        # Check that some text was extracted
        assert isinstance(text, str)
        assert len(text) > 0
        
        # Check for expected content (case-insensitive)
        text_lower = text.lower()
        assert "green grocery" in text_lower or "grocery" in text_lower
    
    def test_extract_text_file_not_found(self):
        """Test text extraction with non-existent file"""
        with pytest.raises(FileNotFoundError):
            self.book._extract_text_from_image("non_existent_file.png")
    
    def test_extract_text_unsupported_format(self):
        """Test text extraction with unsupported format"""
        # Create a dummy file with unsupported extension
        dummy_file = "test_dummy.txt"
        with open(dummy_file, "w") as f:
            f.write("dummy content")
        
        try:
            with pytest.raises(ValueError, match="Unsupported image format"):
                self.book._extract_text_from_image(dummy_file)
        finally:
            if os.path.exists(dummy_file):
                os.remove(dummy_file)
    
    def test_extract_text_pdf_not_supported(self):
        """Test that PDF format raises appropriate error"""
        # Create a dummy PDF file
        dummy_pdf = "test_dummy.pdf"
        with open(dummy_pdf, "w") as f:
            f.write("dummy pdf content")
        
        try:
            with pytest.raises(ValueError, match="PDF support not implemented"):
                self.book._extract_text_from_image(dummy_pdf)
        finally:
            if os.path.exists(dummy_pdf):
                os.remove(dummy_pdf)
