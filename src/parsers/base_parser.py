"""
Base functions and constants for parsers.
"""
from src.utils.helpers import find_section_by_optimized_path

# Common path to the structured body of the document
SUB_PATH = ['component', 'structuredBody', 'component', 'section']

def get_full_path(short_path):
    """
    Gets full path by adding SUB_PATH to the short path.
    
    Args:
        short_path: Short path to the section
        
    Returns:
        list: Full path to the section
    """
    return SUB_PATH + short_path 