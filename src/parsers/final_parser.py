"""
Парсер для финальных таблиц.
"""
from src.utils.helpers import find_section_by_optimized_path
from src.utils.table_utils import parse_table_2
from src.parsers.base_parser import BaseParser, SUB_PATH


class FinalParser:
    """
    Парсер для извлечения информации из финальных таблиц медицинских документов.
    """
    
    @staticmethod
    def get_final_table1(data, type='table'):
        """
        Извлекает первую финальную таблицу из данных.
        
        Args:
            data: JSON данные документа
            type: Тип возвращаемых данных ('table' - DataFrame, 'raw' - JSON)
            
        Returns:
            DataFrame или dict: Финальная таблица 1
        """
        short_path_to_section = ['component', 4, 
                                'section', 
                                'text']
    
        section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
        table = section_fields
        if type == 'table':
            table = parse_table_2(section_fields)
        return table
    
    @staticmethod
    def get_final_table2(data, type='table'):
        """
        Извлекает вторую финальную таблицу из данных.
        
        Args:
            data: JSON данные документа
            type: Тип возвращаемых данных ('table' - DataFrame, 'raw' - JSON)
            
        Returns:
            DataFrame или dict: Финальная таблица 2
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