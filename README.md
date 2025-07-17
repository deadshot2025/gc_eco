# GC-ECO Bookkeeping System

GC-ECO is a Python-based bookkeeping system that provides Excel template-based transaction management with automated routing capabilities. The system is designed to simplify financial record-keeping by automatically categorizing transactions based on configurable tags and maintaining tax rate information.

## Features

- **Excel Template-Based Bookkeeping**: Uses a structured Excel template for data storage and organization
- **Tag-Based Routing**: Automatically routes transactions to appropriate sheets (SALES, EXPENSES) based on description keywords
- **Tax Rate Management**: Integrated VAT, CIT, and USC rate management with JSON configuration
- **Raw Data Processing**: Load and process raw transaction data from CSV or DataFrame sources
- **Metadata Integration**: Stores and manages tax rates and system metadata within the Excel workbook

## Installation

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install required dependencies**:
   ```bash
   pip install pandas openpyxl pytest
   ```

3. **Clone or download the project** and ensure the following files are present:
   - `book.py` - Main application code
   - `data/GC_ECO_Template.xlsx` - Excel template
   - `data/vat_cit_usc_rates.json` - Tax rates configuration
   - `tag_map.md` - Tag to sheet mapping configuration

## Usage

### Basic Usage

Run the main application:
```bash
python book.py
```

### Programmatic Usage

```python
from book import GCEcoBook
import pandas as pd

# Create a GC-ECO book instance
book = GCEcoBook()

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
│   └── receipts/                   # Directory for receipt data files
├── tests/
│   └── test_book.py                # Test suite
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
- **test_meta_loaded()**: Verifies metadata loading from JSON configuration
- **test_routing()**: Tests transaction routing functionality

## Excel Template Structure

The system uses a structured Excel template with the following sheets:

- **RAW**: Temporary storage for unprocessed transactions
- **SALES**: Sales and income transactions
- **EXPENSES**: Expense and purchase transactions  
- **GC_META**: System metadata and configuration storage

## Example Usage

1. **Prepare your transaction data** in CSV format with columns: Date, Description, Amount, VATRate, Tags
2. **Run the system** to load and process transactions:
   ```python
   book = GCEcoBook()
   df = pd.read_csv('your_transactions.csv')
   book.load_raw(df)
   book.route_raw()
   ```
3. **Check the Excel file** (`data/GC_ECO_Template.xlsx`) to see your transactions automatically categorized

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
