"""
Parser for hospitalization information.
"""
from src.utils.helpers import find_section_by_optimized_path
from src.utils.table_utils import parse_table, parse_table_2, parse_table_wtheader
from src.parsers.base_parser import BaseParser, SUB_PATH


def get_gosp_info(data, type='table'):
    """
    Extracts hospitalization information from data.
    
    Args:
        data: Document JSON data
        type: Type of returned data ('table' - DataFrame, 'raw' - JSON)
        
    Returns:
        tuple: (table, type_gosp, way_gosp) - table, hospitalization type, hospitalization route
    """
    short_path_to_section = ['text']
    
    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    table = section_fields
    if type == 'table':
        table = parse_table(section_fields)

    short_path_to_section = ['entry', 2, 
                            'observation', 
                            'value']
    
    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    type_gosp = section_fields['displayName']

    short_path_to_section = ['entry', 3, 
                            'observation', 
                            'value']
    
    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    way_gosp = section_fields['displayName']

    return table, type_gosp, way_gosp

def get_diagnosis(data, type='table'):
    """
    Extracts diagnosis from data.
    
    Args:
        data: Document JSON data
        type: Type of returned data ('table' - DataFrame, 'raw' - JSON)
        
    Returns:
        DataFrame or dict: Diagnosis table
    """
    short_path_to_section = ['component', 1, 
                            'section', 
                            'component', 
                            'section', 
                            'text']

    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    table = section_fields
    if type == 'table':
        table = parse_table(section_fields)

    return table 