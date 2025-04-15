"""
Medical data parsing module for XML/JSON formats.

This package provides tools for:
1. Parsing and extracting data from XML and JSON files
2. Converting between file formats
3. Processing medical records
4. Analyzing medical data
"""

# Make key components available at package level
from src.io.file_converter import xml_to_json, process_files_in_directory
from src.io.data_processor import (
    modify_json,
    save_features,
    process_data_to_structured_format,
    process_folder_to_structured_format
) 