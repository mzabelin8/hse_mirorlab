from src.parser_fucn import *


SUB_PATH = ['component', 'structuredBody', 'component', 'section']

def get_sex(data):
    short_path_to_section = ['recordTarget', 
                             'patientRole', 
                             'patient', 
                             'administrativeGenderCode']
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)

    return section_fields['displayName']


def get_age(data):
    short_path_to_section = ['recordTarget', 
                             'patientRole', 
                             'patient', 
                             'birthTime']
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)

    return section_fields['value']

def get_gosp_info(data, type='table'):
    # type of table data {table - table, raw - raw json}
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
def get_amnez_d(data):
    short_path_to_section = ['component', 0, 
                             'section', 
                             'text']
    
    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)

    return section_fields['text']


def get_condition(data):
    short_path_to_section = ['component', 1, 
                             'section', 
                             'text', 
                             'content']
    
    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)

    result = []
    for el in section_fields:
        result.append(el['text'])

    return result



def get_ward_table(data, type='table'):
    short_path_to_section = ['component', 3, 
                             'section', 
                             'text']


    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    table = section_fields
    if type == 'table':
        table = parse_table(section_fields)
    return table


def get_amnez_life(data):
    short_path_to_section = ['component', 2,
                             'section', 
                             'text']


    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)

    return section_fields['text']

def get_ward_list(data):
    '''
    Вся информация по отдлениям.
    '''
    short_path_to_section = ['component', 3, 
                             'section', 
                             'component']


    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    return section_fields


    


def get_ward_name(data, i):
    short_path_to_section = [i, 'section', 'title']


    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    return section_fields['text']




def get_research_list(data, i):

    """
    Всегда ли лист возвращается?
    """
    short_path_to_section = [i, 'section']

    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    if '{urn:hl7-org:v3}component' in section_fields.keys():
        short_path_to_section = ['component', 'section', 'component']
        section_fields = find_section_by_optimized_path(section_fields, short_path_to_section)
        return section_fields
    return None

def get_research_name(data, i):
    short_path_to_section = ['section', 'title']
    if type(data) == list:
        short_path_to_section = [i, 'section', 'title']

    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    return section_fields['text']

def get_research_table(data, i, typed='table'):
    short_path_to_section = ['section', 'text']

    if type(data) == list:
        short_path_to_section = [i, 'section', 'text']

    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    if typed != 'table':
        return section_fields
        
    table = parse_table_wtheader(section_fields)
    
    return table

def compute_full_wards(data):
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



def get_final_table1(data, type='table'):
    short_path_to_section = ['component', 4, 
                             'section', 
                             'text']

    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    table = section_fields
    if type == 'table':
        table = parse_table_2(section_fields)
    return table


def get_final_table2(data, type='table'):
    short_path_to_section = ['component', 4,
                             'section',
                             'component', 
                             'section', 'text']

    section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
    table = section_fields
    if type == 'table':
        table = parse_table_2(section_fields)
    return table