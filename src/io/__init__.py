"""
Input/output file operations module.

This module contains functionality for:
- Converting between XML and JSON formats
- Processing medical data files
- Saving and loading structured data
"""

from src.io.file_converter import xml_to_json, process_files_in_directory
from src.io.data_processor import (
    modify_json,
    save_features,
    process_data_to_structured_format,
    process_file_to_structured_format,
    process_folder_to_structured_format
) 