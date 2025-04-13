"""
Парсер для информации о госпитализации.
"""
from src.utils.helpers import find_section_by_optimized_path
from src.utils.table_utils import parse_table, parse_table_2, parse_table_wtheader
from src.parsers.base_parser import BaseParser, SUB_PATH


class HospParser:
    """
    Парсер для извлечения информации о госпитализации из медицинских документов.
    """
    
    @staticmethod
    def get_gosp_info(data, type='table'):
        """
        Извлекает информацию о госпитализации из данных.
        
        Args:
            data: JSON данные документа
            type: Тип возвращаемых данных ('table' - DataFrame, 'raw' - JSON)
            
        Returns:
            tuple: (table, type_gosp, way_gosp) - таблица, тип госпитализации, путь госпитализации
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
    
    @staticmethod
    def get_diagnosis(data, type='table'):
        """
        Извлекает диагноз из данных.
        
        Args:
            data: JSON данные документа
            type: Тип возвращаемых данных ('table' - DataFrame, 'raw' - JSON)
            
        Returns:
            DataFrame или dict: Таблица с диагнозом
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