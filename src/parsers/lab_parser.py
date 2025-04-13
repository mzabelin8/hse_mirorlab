"""
Парсер для лабораторных данных.
"""
from src.utils.helpers import find_section_by_optimized_path
from src.utils.table_utils import convert_table_to_dataframe


class LabParser:
    """
    Парсер для извлечения лабораторных данных из медицинских документов.
    """
    
    @staticmethod
    def get_table_1(data):
        """
        Извлекает таблицу лабораторных данных из документа.
        
        Args:
            data: JSON данные документа
            
        Returns:
            DataFrame: Таблица лабораторных данных
        """
        short_path_to_section = ['component', 
                               'structuredBody', 
                               'component', 2, 
                               'section', 'text']
        
        section_fields = find_section_by_optimized_path(data, short_path_to_section)
        table = convert_table_to_dataframe(section_fields)
    
        return table 