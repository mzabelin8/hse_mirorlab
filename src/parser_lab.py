from src.parser_fucn import *

def get_table_1(data):
    short_path_to_section = ['component', 
                             'structuredBody', 
                             'component', 2, 
                             'section', 'text']
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    table = convert_table_to_dataframe(section_fields)

    return table
