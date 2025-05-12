"""
Parser for patient information.
"""
from src.utils.helpers import find_section_by_optimized_path
from src.parsers.base_parser import SUB_PATH


def get_sex(data):
    """
    Extracts patient gender from data.
    
    Args:
        data: Document JSON data
        
    Returns:
        str: Patient gender
    """
    short_path_to_section = ['recordTarget', 
                            'patientRole', 
                            'patient', 
                            'administrativeGenderCode']
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    return section_fields['displayName']

def get_age(data):
    """
    Extracts patient age/birth date from data.
    
    Args:
        data: Document JSON data
        
    Returns:
        str: Patient birth date
    """
    short_path_to_section = ['recordTarget', 
                            'patientRole', 
                            'patient', 
                            'birthTime']
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    return section_fields['value']

def get_id(data):
    """
    Extracts patient ID from data.
    
    Args:
        data: Document JSON data
        
    Returns:
        str: Patient ID extension
    """
    short_path_to_section = ['recordTarget', 
                            'patientRole', 
                            'id', 0]
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    return section_fields['extension']

def get_amnez_d(data):
    """
    Extracts disease anamnesis from data.
    
    Args:
        data: Document JSON data
        
    Returns:
        str: Disease anamnesis
    """
    short_path_to_section = ['component', 0, 
                            'section', 
                            'text']
    
    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    return section_fields['text']

def get_amnez_life(data):
    """
    Extracts life anamnesis from data.
    
    Args:
        data: Document JSON data
        
    Returns:
        str: Life anamnesis
    """
    short_path_to_section = ['component', 2,
                            'section', 
                            'text']
    
    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    return section_fields['text']

def get_condition(data):
    """
    Extracts patient condition from data.
    
    Args:
        data: Document JSON data
        
    Returns:
        list: Patient condition
    """
    short_path_to_section = ['component', 1, 
                            'section', 
                            'text', 
                            'content']
    
    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    
    result = []
    for el in section_fields:
        result.append(el['text'])
        
    return result

def parse_conditions_as_key_value(conditions):
    """
    Parses each condition line as 'key: value' if possible.
    
    Args:
        conditions: List of condition strings
        
    Returns:
        dict: Structured dictionary with conditions
    """
    structured = {}

    for line in conditions:
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            structured[key] = value
        else:
            # If the string doesn't contain ":", record it as is
            structured[line.strip()] = None

    return structured

def get_structured_condition(data):
    """
    Extracts structured patient condition from data.
    
    Args:
        data: Document JSON data
        
    Returns:
        dict: Structured patient condition
    """
    conditions = get_condition(data)
    return parse_conditions_as_key_value(conditions) 