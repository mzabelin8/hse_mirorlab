"""
Parser for final tables.
"""
from src.utils.helpers import find_section_by_optimized_path
from src.utils.table_utils import parse_table_2
from src.parsers.base_parser import SUB_PATH


def get_final_table1(data, type='table'):
    """
    Extracts the first final table from data.
    
    Args:
        data: Document JSON data
        type: Type of returned data ('table' - DataFrame, 'raw' - JSON)
        
    Returns:
        DataFrame or dict: Final table 1
    """
    short_path_to_section = ['component', 4, 
                            'section', 
                            'text']

    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    table = section_fields
    if type == 'table':
        table = parse_table_2(section_fields)
    return table

def get_final_table2(data, type='table'):
    """
    Extracts the second final table from data.
    
    Args:
        data: Document JSON data
        type: Type of returned data ('table' - DataFrame, 'raw' - JSON)
        
    Returns:
        DataFrame or dict: Final table 2
    """
    short_path_to_section = ['component', 4,
                            'section',
                            'component', 
                            'section', 'text']

    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    table = section_fields
    if type == 'table':
        table = parse_table_2(section_fields)
    return table 