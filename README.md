# Medical Data Parser

A library for parsing and extracting structured information from medical XML/JSON documents.

## Project Structure

```
src/
├── __init__.py
├── io/                      # File operations module
│   ├── __init__.py
│   ├── file_converter.py    # XML to JSON conversion
│   └── data_processor.py    # Data processing and saving
├── parsers/                 # Parsers module
│   ├── __init__.py
│   ├── base_parser.py       # Base functions for parsers
│   ├── patient_parser.py    # Patient data parser
│   ├── hosp_parser.py       # Hospitalization data parser
│   ├── ward_parser.py       # Department data parser
│   ├── final_parser.py      # Final tables parser
│   └── lab_parser.py        # Laboratory data parser
└── utils/                   # Utilities
    ├── __init__.py
    ├── helpers.py           # Helper functions
    └── table_utils.py       # Functions for working with tables
```

## Usage Examples

### Converting XML File to JSON

```python
from src.io.file_converter import xml_to_json

xml_to_json('path/to/file.xml', 'path/to/output.json')
```

### Processing All XML Files in a Directory

```python
from src.io.file_converter import process_files_in_directory

process_files_in_directory('input_directory', 'output_directory')
```

### Extracting Structured Data from JSON

```python
from src.io.data_processor import modify_json

modify_json('path/to/json_file.json', 'path/to/output.json')
```

### Using Individual Parsers

```python
import json
from src.parsers.patient_parser import get_sex
from src.parsers.hosp_parser import get_gosp_info

# Load data
with open('path/to/json_file.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract patient gender
sex = get_sex(data)

# Extract hospitalization information
table, type_gosp, way_gosp = get_gosp_info(data)
```

### Processing All Files

To process all files in a directory and save the results:

```python
from src.io.data_processor import save_features

save_features('input_json_directory', 'output_features_directory')
```

### Processing Files into Structured Format

```python
from src.io.data_processor import process_folder_to_structured_format

stats = process_folder_to_structured_format('input_json_directory', 'output_structured_directory')
print(f"Processed {stats['total']} files with {stats['success']} successes and {stats['errors']} errors")
```

## Working with Tables

The library provides several functions for working with tabular data:

```python
from src.utils.table_utils import safe_parse_table, save_table_as_dict

# Parse a table from JSON data
table_df = safe_parse_table(table_data)

# Convert DataFrame to dictionary
table_dict = save_table_as_dict(table_df)
```

