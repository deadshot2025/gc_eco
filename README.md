# GC-ECO Bookkeeping System

GC-ECO is a Python-based bookkeeping system that provides Excel template-based transaction management with automated routing capabilities. The system is designed to simplify financial record-keeping by automatically categorizing transactions based on configurable tags and maintaining tax rate information.

## Features

- **Excel Template-Based Bookkeeping**: Uses a structured Excel template for data storage and organization
- **OCR Receipt Processing**: Extract transaction data from receipt images using Tesseract OCR
- **Batch Receipt Processing**: Process multiple receipt images from a folder automatically
- **Tag-Based Routing**: Automatically routes transactions to appropriate sheets (SALES, EXPENSES) based on description keywords
- **Tax Rate Management**: Integrated VAT, CIT, and USC rate management with JSON configuration
- **Raw Data Processing**: Load and process raw transaction data from CSV or DataFrame sources
- **Metadata Integration**: Stores and manages tax rates and system metadata within the Excel workbook
- **Image Preprocessing**: Automatic image enhancement for improved OCR accuracy
- **Smart Data Extraction**: Intelligent parsing of dates, amounts, VAT rates, and merchant information from receipts

## Installation

### Prerequisites

**Install Tesseract OCR** (required for receipt processing):

```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
```

### Python Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install pandas openpyxl pytest pytesseract Pillow opencv-python
   ```

3. **Clone or download the project** and ensure the following files are present:
   - `book.py` - Main application code
   - `data/GC_ECO_Template.xlsx` - Excel template
   - `data/vat_cit_usc_rates.json` - Tax rates configuration
   - `tag_map.md` - Tag to sheet mapping configuration
   - `data/receipts/` - Directory for receipt images

## Usage

### Basic Usage

Run the main application to see OCR processing demo:
```bash
python book.py
```

### OCR Receipt Processing

#### Single Receipt Processing

```python
from book import GCEcoBook

# Create a GC-ECO book instance
book = GCEcoBook()

# Process a single receipt image
receipt_data = book.process_receipt_image("data/receipts/receipt.png")

print(f"Date: {receipt_data['Date']}")
print(f"Description: {receipt_data['Description']}")
print(f"Amount: €{receipt_data['Amount']}")
print(f"VAT Rate: {receipt_data['VATRate']}%")
print(f"Tags: {receipt_data['Tags']}")
```

#### Batch Receipt Processing

```python
# Process all receipt images in a folder
df = book.process_receipts_folder("data/receipts")

# Load the extracted data into the system
book.load_raw(df)

# Route transactions to appropriate sheets based on tags
book.route_raw()

# Save the workbook
book.save()
```

#### Complete OCR Workflow

```python
from book import GCEcoBook

# Create instance
book = GCEcoBook()

# Process receipts → extract data → load → route → save
df = book.process_receipts_folder("data/receipts")
book.load_raw(df)
book.route_raw()
book.save()

print(f"Processed {len(df)} receipts successfully!")
```

### Manual Data Entry

```python
import pandas as pd

# Load raw transaction data from a DataFrame
df = pd.DataFrame([{
    "Date": "2025-07-01",
    "Description": "office supplies expense",
    "Amount": 150.00,
    "VATRate": 23,
    "Tags": ""
}])

# Load the raw data into the system
book.load_raw(df)

# Route transactions to appropriate sheets based on tags
book.route_raw()

# Save the workbook
book.save()
```

### Loading from CSV

```python
# Load transactions from a CSV file
df = pd.read_csv('data/receipts/sample_receipts.csv')
book.load_raw(df)
book.route_raw()
```

## Project Structure

```
gc_eco/
├── book.py                          # Main application code
├── data/
│   ├── GC_ECO_Template.xlsx        # Excel template with sheets: RAW, SALES, EXPENSES, GC_META
│   ├── vat_cit_usc_rates.json      # Tax rates configuration
│   └── receipts/                   # Directory for receipt images (PNG, JPG, etc.)
│       └── test_receipt.png        # Sample receipt for testing
├── tests/
│   ├── test_book.py                # Core functionality tests
│   ├── test_ocr.py                 # OCR functionality tests
│   └── test_receipt_processing.py  # Receipt processing tests
├── requirements.txt                # Python dependencies
├── tag_map.md                      # Tag to sheet mapping configuration
├── README.md                       # This file
└── LICENSE                         # MIT License
```

## Configuration

### Tax Rates (`data/vat_cit_usc_rates.json`)
Configure VAT, CIT, and USC rates:
```json
{
  "VAT": {
    "standard": 23,
    "reduced": 8,
    "zero": 0
  },
  "CIT": {
    "standard": 19,
    "small_business": 9
  },
  "USC": {
    "rate": 4.5
  }
}
```

### Tag Mapping (`tag_map.md`)
Configure how transaction descriptions are routed to sheets:
```markdown
| tag | target_sheet |
|----------|--------------| 
| sales | SALES |
| income | SALES |
| expenses | EXPENSES |
| purchase | EXPENSES |
```

## Testing

Run the test suite to verify functionality:
```bash
pytest -q
```

The test suite includes:

### Core Functionality Tests (`test_book.py`)
- **test_meta_loaded()**: Verifies metadata loading from JSON configuration
- **test_routing()**: Tests transaction routing functionality

### OCR Tests (`test_ocr.py`)
- **test_preprocess_image_success()**: Tests image preprocessing for OCR
- **test_extract_text_success()**: Tests text extraction from images
- **test_extract_text_file_not_found()**: Tests error handling for missing files
- **test_preprocess_image_unsupported_format()**: Tests unsupported file format handling

### Receipt Processing Tests (`test_receipt_processing.py`)
- **test_extract_receipt_data_basic()**: Tests structured data extraction from OCR text
- **test_extract_receipt_data_different_formats()**: Tests various date/amount formats
- **test_extract_receipt_data_vat_detection()**: Tests VAT rate detection
- **test_process_receipt_image_success()**: Tests end-to-end receipt processing
- **test_process_receipts_folder_success()**: Tests batch processing functionality
- **test_integration_with_existing_system()**: Tests OCR integration with routing system

## Excel Template Structure

The system uses a structured Excel template with the following sheets:

- **RAW**: Temporary storage for unprocessed transactions
- **SALES**: Sales and income transactions
- **EXPENSES**: Expense and purchase transactions  
- **GC_META**: System metadata and configuration storage

## Example Usage

### OCR Receipt Processing Workflow

1. **Place receipt images** in the `data/receipts/` folder (supports PNG, JPG, JPEG, BMP, TIFF)
2. **Run the OCR processing**:
   ```python
   from book import GCEcoBook
   
   book = GCEcoBook()
   df = book.process_receipts_folder("data/receipts")
   book.load_raw(df)
   book.route_raw()
   book.save()
   ```
3. **Check the Excel file** (`data/GC_ECO_Template.xlsx`) to see your receipt transactions automatically categorized

### Manual Data Entry Workflow

1. **Prepare your transaction data** in CSV format with columns: Date, Description, Amount, VATRate, Tags
2. **Run the system** to load and process transactions:
   ```python
   book = GCEcoBook()
   df = pd.read_csv('your_transactions.csv')
   book.load_raw(df)
   book.route_raw()
   ```
3. **Check the Excel file** to see your transactions automatically categorized

## Troubleshooting

### OCR Issues

**Tesseract not found error:**
```
TesseractNotFoundError: tesseract is not installed or it's not in your PATH
```
**Solution:** Install Tesseract OCR using the installation instructions above.

**Poor OCR accuracy:**
- Ensure receipt images are clear and well-lit
- Supported formats: PNG, JPG, JPEG, BMP, TIFF
- The system automatically preprocesses images for better accuracy
- Try scanning receipts at higher resolution (300 DPI recommended)

**No text extracted from image:**
- Check if the image file is corrupted
- Verify the image contains readable text
- Ensure the image is not too blurry or dark

**Date/Amount not detected:**
- The system uses pattern matching for common receipt formats
- Manually verify extracted data in the Excel output
- Consider updating the regex patterns in `_extract_receipt_data()` for specific receipt formats

**Batch processing errors:**
- Check file permissions in the receipts folder
- Ensure all images are valid image files
- The system will skip corrupted files and continue processing

### General Issues

**Excel file locked:**
- Close the Excel file before running the system
- The system needs write access to update the template

**Import errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version compatibility (Python 3.7+)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
