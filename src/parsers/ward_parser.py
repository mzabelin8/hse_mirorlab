"""
Parser for department information.
"""
from src.utils.helpers import find_section_by_optimized_path
from src.utils.table_utils import parse_table, parse_table_2, parse_table_wtheader
from src.parsers.base_parser import SUB_PATH


def get_ward_table(data, type='table'):
    """
    Extracts department table from data.
    
    Args:
        data: Document JSON data
        type: Type of returned data ('table' - DataFrame, 'raw' - JSON)
        
    Returns:
        DataFrame or dict: Department table
    """
    short_path_to_section = ['component', 3, 
                            'section', 
                            'text']

    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    table = section_fields
    if type == 'table':
        table = parse_table(section_fields)
    return table

def get_ward_list(data):
    """
    Extracts information for all departments.
    
    Args:
        data: Document JSON data
        
    Returns:
        list: List of departments
    """
    short_path_to_section = ['component', 3, 
                            'section', 
                            'component']

    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    return section_fields

def get_ward_name(data, i):
    """
    Extracts department name by index.
    
    Args:
        data: Department data
        i: Department index
        
    Returns:
        str: Department name
    """
    short_path_to_section = [i, 'section', 'title']

    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    return section_fields['text']

def get_research_list(data, i):
    """
    Extracts list of examinations in the department.
    
    Args:
        data: Department data
        i: Department index
        
    Returns:
        list: List of examinations or None
    """
    short_path_to_section = [i, 'section']

    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    if '{urn:hl7-org:v3}component' in section_fields.keys():
        short_path_to_section = ['component', 'section', 'component']
        section_fields = find_section_by_optimized_path(section_fields, short_path_to_section)
        return section_fields
    return None

def get_research_name(data, i):
    """
    Extracts examination name by index.
    
    Args:
        data: Examination data
        i: Examination index
        
    Returns:
        str: Examination name
    """
    short_path_to_section = ['section', 'title']
    if type(data) == list:
        short_path_to_section = [i, 'section', 'title']

    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    return section_fields['text']

def get_research_table(data, i, typed='table'):
    """
    Extracts examination table by index.
    
    Args:
        data: Examination data
        i: Examination index
        typed: Type of returned data ('table' - DataFrame, 'r' - JSON)
        
    Returns:
        DataFrame or dict: Examination table
    """
    short_path_to_section = ['section', 'text']

    if type(data) == list:
        short_path_to_section = [i, 'section', 'text']

    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    if typed != 'table':
        return section_fields
        
    table = parse_table_wtheader(section_fields)
    
    return table

def compute_full_wards(data):
    """
    Computes full information for all departments.
    
    Args:
        data: Document JSON data
        
    Returns:
        dict: Dictionary with department information
    """
    ward_result = {}
    
    ward_list = get_ward_list(data)

    for i in range(len(ward_list)):
        ward_name = get_ward_name(ward_list, i)

        res_list = get_research_list(ward_list, i)
        research_result = {}
        if res_list:
            for j in range(len(res_list)):
                res_name = get_research_name(res_list, j)
                res_table = get_research_table(res_list, j, 'r')
                research_result[res_name] = res_table

        ward_result[ward_name] = research_result
    return ward_result 