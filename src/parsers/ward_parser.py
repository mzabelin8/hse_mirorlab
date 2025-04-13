"""
Парсер для информации об отделениях.
"""
from src.utils.helpers import find_section_by_optimized_path
from src.utils.table_utils import parse_table, parse_table_2, parse_table_wtheader
from src.parsers.base_parser import BaseParser, SUB_PATH


class WardParser:
    """
    Парсер для извлечения информации об отделениях из медицинских документов.
    """
    
    @staticmethod
    def get_ward_table(data, type='table'):
        """
        Извлекает таблицу отделений из данных.
        
        Args:
            data: JSON данные документа
            type: Тип возвращаемых данных ('table' - DataFrame, 'raw' - JSON)
            
        Returns:
            DataFrame или dict: Таблица отделений
        """
        short_path_to_section = ['component', 3, 
                                'section', 
                                'text']
    
        section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
        table = section_fields
        if type == 'table':
            table = parse_table(section_fields)
        return table
    
    @staticmethod
    def get_ward_list(data):
        """
        Извлекает информацию по всем отделениям.
        
        Args:
            data: JSON данные документа
            
        Returns:
            list: Список отделений
        """
        short_path_to_section = ['component', 3, 
                                'section', 
                                'component']
    
        section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
        return section_fields
    
    @staticmethod
    def get_ward_name(data, i):
        """
        Извлекает название отделения по индексу.
        
        Args:
            data: Данные об отделениях
            i: Индекс отделения
            
        Returns:
            str: Название отделения
        """
        short_path_to_section = [i, 'section', 'title']
    
        section_fields = find_section_by_optimized_path(data, short_path_to_section)
        return section_fields['text']
    
    @staticmethod
    def get_research_list(data, i):
        """
        Извлекает список исследований в отделении.
        
        Args:
            data: Данные об отделениях
            i: Индекс отделения
            
        Returns:
            list: Список исследований или None
        """
        short_path_to_section = [i, 'section']
    
        section_fields = find_section_by_optimized_path(data, short_path_to_section)
        if '{urn:hl7-org:v3}component' in section_fields.keys():
            short_path_to_section = ['component', 'section', 'component']
            section_fields = find_section_by_optimized_path(section_fields, short_path_to_section)
            return section_fields
        return None
    
    @staticmethod
    def get_research_name(data, i):
        """
        Извлекает название исследования по индексу.
        
        Args:
            data: Данные об исследованиях
            i: Индекс исследования
            
        Returns:
            str: Название исследования
        """
        short_path_to_section = ['section', 'title']
        if type(data) == list:
            short_path_to_section = [i, 'section', 'title']
    
        section_fields = find_section_by_optimized_path(data, short_path_to_section)
        return section_fields['text']
    
    @staticmethod
    def get_research_table(data, i, typed='table'):
        """
        Извлекает таблицу исследования по индексу.
        
        Args:
            data: Данные об исследованиях
            i: Индекс исследования
            typed: Тип возвращаемых данных ('table' - DataFrame, 'r' - JSON)
            
        Returns:
            DataFrame или dict: Таблица исследования
        """
        short_path_to_section = ['section', 'text']
    
        if type(data) == list:
            short_path_to_section = [i, 'section', 'text']
    
        section_fields = find_section_by_optimized_path(data, short_path_to_section)
        if typed != 'table':
            return section_fields
            
        table = parse_table_wtheader(section_fields)
        
        return table
    
    @staticmethod
    def compute_full_wards(data):
        """
        Вычисляет полную информацию по всем отделениям.
        
        Args:
            data: JSON данные документа
            
        Returns:
            dict: Словарь с информацией по отделениям
        """
        ward_result = {}
        
        ward_list = WardParser.get_ward_list(data)
    
        for i in range(len(ward_list)):
            ward_name = WardParser.get_ward_name(ward_list, i)
    
            res_list = WardParser.get_research_list(ward_list, i)
            research_result = {}
            if res_list:
                for j in range(len(res_list)):
                    res_name = WardParser.get_research_name(res_list, j)
                    res_table = WardParser.get_research_table(res_list, j, 'r')
                    research_result[res_name] = res_table
    
            ward_result[ward_name] = research_result
        return ward_result 