"""
Базовые функции и константы для парсеров.
"""
from src.utils.helpers import find_section_by_optimized_path

# Общий путь к структурированному телу документа
SUB_PATH = ['component', 'structuredBody', 'component', 'section']

class BaseParser:
    """
    Базовый класс для парсеров.
    Содержит общую функциональность, используемую во всех парсерах.
    """
    
    @staticmethod
    def get_full_path(short_path):
        """
        Получает полный путь, добавляя SUB_PATH к короткому пути.
        
        Args:
            short_path: Короткий путь к секции
            
        Returns:
            list: Полный путь к секции
        """
        return SUB_PATH + short_path 