"""
Helper functions for data processing.
"""
import pandas as pd


def find_section_by_optimized_path(data, short_path, fields=None, prefix='{urn:hl7-org:v3}'):
    """
    Navigate through nested JSON structure by specified path, automatically adding a prefix to string path elements.
    Optionally returns only specified fields from the final block.

    Args:
        data: JSON data as a nested Python dictionary.
        short_path: Simplified path to the desired section as a list of keys and indices.
        fields: Optional. Tuple or list of field names to return from the final block.
                If None, returns the entire block.
        prefix: Prefix added to string path elements.
    
    Returns:
        The section at the specified path, or specific fields from the section, or None if the path is invalid.
    """
    current = data
    full_path = [(prefix + element) if isinstance(element, str)
                 else element for element in short_path]

    try:
        for key in full_path:
            if isinstance(current, list):  # Handle list indices
                current = current[int(key)]
            else:  # Handle dictionary keys
                current = current[key]

        if fields and isinstance(fields, (list, tuple)) and isinstance(current, dict):
            return {field: current.get(field, None) for field in fields}

        return current
    except (KeyError, IndexError, ValueError, TypeError):
        return None  # Path is invalid


def clean_keys(obj):
    """
    Recursively removes namespace prefixes from dictionary keys.
    
    Args:
        obj: Object (dictionary, list, or scalar) to process
        
    Returns:
        Object with cleaned keys
    """
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            new_key = key
            if key.startswith('{'):
                new_key = key[key.find('}')+1:]
            new_dict[new_key] = clean_keys(value)
        return new_dict
    elif isinstance(obj, list):
        return [clean_keys(item) for item in obj]
    else:
        return obj 