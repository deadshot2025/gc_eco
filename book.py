import json
import pandas as pd
from openpyxl import load_workbook

# Constants
TEMPLATE_PATH = "data/GC_ECO_Template.xlsx"
RATES_PATH = "data/vat_cit_usc_rates.json"
TAGMAP_PATH = "tag_map.md"


class GCEcoBook:
    def __init__(self):
        # Load the Excel workbook from TEMPLATE_PATH using openpyxl
        self.workbook = load_workbook(TEMPLATE_PATH)
        
        # Load JSON metadata from RATES_PATH into self.meta
        with open(RATES_PATH, 'r') as f:
            self.meta = json.load(f)
        
        # Call self._write_meta() to write metadata to Excel
        self._write_meta()
        
        # Load tag mapping from TAGMAP_PATH using pandas
        # Skip first row, use columns 1,2, handle markdown table format with regex separator
        tag_df = pd.read_csv(TAGMAP_PATH, sep=r"\s*\|\s*", engine='python', 
                            skiprows=1, usecols=[1, 2], names=['tag', 'target_sheet'])
        
        # Filter out the markdown separator row (contains dashes)
        tag_df = tag_df[~tag_df['tag'].str.contains('-', na=False)]
        
        # Create self.tag_map dictionary from tag->target_sheet mapping
        self.tag_map = dict(zip(tag_df['tag'], tag_df['target_sheet']))
    
    def _write_meta(self):
        # Get the GC_META worksheet
        meta_sheet = self.workbook['GC_META']
        
        # Write JSON-serialized self.meta to cell A1
        meta_sheet['A1'] = json.dumps(self.meta)
    
    def save(self):
        # Save the workbook to TEMPLATE_PATH
        self.workbook.save(TEMPLATE_PATH)
    
    def load_raw(self, df_raw: pd.DataFrame):
        # Get the RAW worksheet
        raw_sheet = self.workbook['RAW']
        
        # Iterate through df_raw rows and append each row as a list to the worksheet
        for _, row in df_raw.iterrows():
            raw_sheet.append(row.tolist())
        
        # Call save()
        self.save()
    
    def route_raw(self):
        # Read RAW worksheet data into a pandas DataFrame
        raw_sheet = self.workbook['RAW']
        
        # Extract all data from the worksheet
        data = []
        for row in raw_sheet.iter_rows(values_only=True):
            if any(cell is not None for cell in row):  # Skip empty rows
                data.append(row)
        
        if not data:
            return  # No data to process
        
        # Extract headers from first row, set as column names
        headers = data[0]
        df_raw = pd.DataFrame(data[1:], columns=headers)
        
        # For each data row, check if any tag from self.tag_map appears in the Description column (case-insensitive)
        for _, row in df_raw.iterrows():
            description = str(row.get('Description', '')).lower()
            
            # Check if any tag appears in the description
            for tag, target_sheet in self.tag_map.items():
                if tag.lower() in description:
                    # If match found, call _append_row() with the target sheet and row data
                    self._append_row(target_sheet, row)
                    break  # Only route to first matching tag
        
        # Call save()
        self.save()
    
    def _append_row(self, sheet: str, row: pd.Series):
        # Get the specified worksheet
        target_sheet = self.workbook[sheet]
        
        # Append the row as a list to the worksheet
        target_sheet.append(row.tolist())


if __name__ == "__main__":
    # Create GCEcoBook instance
    book = GCEcoBook()
    
    # Example usage for loading CSV and routing (commented)
    # df = pd.read_csv('data/receipts/sample_receipts.csv')
    # book.load_raw(df)
    # book.route_raw()
    
    # Call save()
    book.save()
