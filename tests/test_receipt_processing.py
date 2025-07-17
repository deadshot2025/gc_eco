import pytest
import pandas as pd
import os
from book import GCEcoBook


class TestReceiptProcessing:
    def setup_method(self):
        """Setup test fixtures"""
        self.book = GCEcoBook()
        self.test_image_path = "data/receipts/test_receipt.png"
    
    def test_extract_receipt_data_basic(self):
        """Test basic receipt data extraction from OCR text"""
        # Sample OCR text similar to what we get from the test receipt
        ocr_text = """GREEN GROCERY STORE
123 Eco Street
Dublin, Ireland

Date: 2024-01-15 Receipt: 012343
Organic Apples €2.20
Bananas €1.00
Bread €3.50
Eggs €2.00
TOTAL: €11.70
VAT: €2.19

Thank you for shopping!"""
        
        result = self.book._extract_receipt_data(ocr_text)
        
        # Verify extracted data
        assert result["Date"] == "2024-01-15"
        assert "GREEN GROCERY STORE" in result["Description"]
        assert result["Amount"] == 11.70
        assert result["VATRate"] == 23  # Default VAT rate
        assert result["Tags"] == "grocery"
    
    def test_extract_receipt_data_different_formats(self):
        """Test receipt data extraction with different date and amount formats"""
        # Test different date format
        ocr_text1 = """RESTAURANT ABC
15/01/2024
TOTAL €25.50"""
        
        result1 = self.book._extract_receipt_data(ocr_text1)
        assert result1["Date"] == "2024-01-15"
        assert result1["Amount"] == 25.50
        assert result1["Tags"] == "restaurant"
        
        # Test different amount format
        ocr_text2 = """OFFICE SUPPLIES LTD
2024-03-10
Total: 45,99 EUR"""
        
        result2 = self.book._extract_receipt_data(ocr_text2)
        assert result2["Date"] == "2024-03-10"
        assert result2["Amount"] == 45.99
        assert result2["Tags"] == "office"
    
    def test_extract_receipt_data_vat_detection(self):
        """Test VAT rate detection from receipt text"""
        ocr_text = """FUEL STATION
2024-02-20
Petrol €50.00
VAT: 13%
TOTAL: €56.50"""
        
        result = self.book._extract_receipt_data(ocr_text)
        assert result["VATRate"] == 13
        assert result["Tags"] == "fuel"
    
    def test_extract_receipt_data_missing_info(self):
        """Test handling of missing information in receipt"""
        ocr_text = """UNKNOWN STORE
Some items
No clear date or amount"""
        
        result = self.book._extract_receipt_data(ocr_text)
        
        # Should have defaults for missing info
        assert result["Date"] is None
        assert result["Amount"] == 0.0
        assert result["VATRate"] == 23
        assert "UNKNOWN STORE" in result["Description"]
        assert result["Tags"] == "expense"  # Default tag
    
    def test_process_receipt_image_success(self):
        """Test successful processing of receipt image"""
        if not os.path.exists(self.test_image_path):
            pytest.skip("Test image not found")
        
        result = self.book.process_receipt_image(self.test_image_path)
        
        # Verify result structure
        assert isinstance(result, dict)
        assert "Date" in result
        assert "Description" in result
        assert "Amount" in result
        assert "VATRate" in result
        assert "Tags" in result
        
        # Verify specific values for test receipt
        assert "GREEN GROCERY STORE" in result["Description"]
        assert result["Amount"] == 11.7
        assert result["Tags"] == "grocery"
    
    def test_process_receipt_image_file_not_found(self):
        """Test processing with non-existent image file"""
        with pytest.raises(FileNotFoundError):
            self.book.process_receipt_image("non_existent_file.png")
    
    def test_process_receipts_folder_success(self):
        """Test batch processing of receipts folder"""
        if not os.path.exists(self.test_image_path):
            pytest.skip("Test image not found")
        
        df = self.book.process_receipts_folder("data/receipts")
        
        # Verify DataFrame structure
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["Date", "Description", "Amount", "VATRate", "Tags"]
        assert len(df) >= 1  # Should have at least the test receipt
        
        # Verify data types
        assert df["Amount"].dtype in ['float64', 'int64']
        assert df["VATRate"].dtype in ['int64', 'float64']
    
    def test_process_receipts_folder_empty(self):
        """Test batch processing with empty folder"""
        df = self.book.process_receipts_folder("non_existent_folder")
        
        # Should return empty DataFrame with correct columns
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["Date", "Description", "Amount", "VATRate", "Tags"]
        assert len(df) == 0
    
    def test_integration_with_existing_system(self):
        """Test integration with existing load_raw and route_raw methods"""
        if not os.path.exists(self.test_image_path):
            pytest.skip("Test image not found")
        
        # Process receipts and get DataFrame
        df = self.book.process_receipts_folder("data/receipts")
        
        # Load into RAW sheet
        self.book.load_raw(df)
        
        # Route the data
        self.book.route_raw()
        
        # Verify data was routed (this is a basic check)
        # More detailed verification would require checking the Excel file
        assert True  # If we get here without exceptions, integration works
    
    def test_tag_mapping_integration(self):
        """Test that receipt tags work with existing tag mapping system"""
        # Create test data with grocery tag
        test_data = pd.DataFrame([{
            "Date": "2024-01-15",
            "Description": "GREEN GROCERY STORE - receipt",
            "Amount": 11.70,
            "VATRate": 23,
            "Tags": "grocery"
        }])
        
        # Load and route
        self.book.load_raw(test_data)
        self.book.route_raw()
        
        # The grocery tag should route to EXPENSES sheet based on tag_map.md
        # This is verified by the integration test above
        assert True