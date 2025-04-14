"""
Parser for laboratory data.
"""
from src.utils.helpers import find_section_by_optimized_path
from src.utils.table_utils import convert_table_to_dataframe


def get_table_1(data):
    """
    Extracts laboratory data table from document.
    
    Args:
        data: Document JSON data
        
    Returns:
        DataFrame: Laboratory data table
    """
    short_path_to_section = ['component', 
                           'structuredBody', 
                           'component', 2, 
                           'section', 'text']
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    table = convert_table_to_dataframe(section_fields)

    return table 