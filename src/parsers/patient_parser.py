"""
Парсер для информации о пациенте.
"""
from src.utils.helpers import find_section_by_optimized_path
from src.parsers.base_parser import BaseParser, SUB_PATH


class PatientParser:
    """
    Парсер для извлечения информации о пациенте из медицинских документов.
    """
    
    @staticmethod
    def get_sex(data):
        """
        Извлекает пол пациента из данных.
        
        Args:
            data: JSON данные документа
            
        Returns:
            str: Пол пациента
        """
        short_path_to_section = ['recordTarget', 
                                'patientRole', 
                                'patient', 
                                'administrativeGenderCode']
        
        section_fields = find_section_by_optimized_path(data, short_path_to_section)
        return section_fields['displayName']

    @staticmethod
    def get_age(data):
        """
        Извлекает возраст/дату рождения пациента из данных.
        
        Args:
            data: JSON данные документа
            
        Returns:
            str: Дата рождения пациента
        """
        short_path_to_section = ['recordTarget', 
                                'patientRole', 
                                'patient', 
                                'birthTime']
        
        section_fields = find_section_by_optimized_path(data, short_path_to_section)
        return section_fields['value']
    
    @staticmethod
    def get_amnez_d(data):
        """
        Извлекает анамнез заболевания из данных.
        
        Args:
            data: JSON данные документа
            
        Returns:
            str: Анамнез заболевания
        """
        short_path_to_section = ['component', 0, 
                                'section', 
                                'text']
        
        section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
        return section_fields['text']
    
    @staticmethod
    def get_amnez_life(data):
        """
        Извлекает анамнез жизни из данных.
        
        Args:
            data: JSON данные документа
            
        Returns:
            str: Анамнез жизни
        """
        short_path_to_section = ['component', 2,
                                'section', 
                                'text']
        
        section_fields = find_section_by_optimized_path(data, SUB_PATH + short_path_to_section)
        return section_fields['text']
    
    @staticmethod
    def get_condition(data):
        """
        Извлекает состояние пациента из данных.
        
        Args:
            data: JSON данные документа
            
        Returns:
            list: Состояние пациента
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
    
    @staticmethod
    def parse_conditions_as_key_value(conditions):
        """
        Парсит каждую строку условия как 'ключ: значение', если возможно.
        
        Args:
            conditions: Список строк с условиями
            
        Returns:
            dict: Структурированный словарь с условиями
        """
        structured = {
            "raw_list": []
        }

        for line in conditions:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                structured[key] = value
                structured["raw_list"].append({
                    "type": key.lower(),
                    "text": value
                })
            else:
                # Если строка не содержит ":", записываем её как есть
                structured["raw_list"].append({
                    "type": "unknown",
                    "text": line.strip()
                })

        return structured
    
    @staticmethod
    def get_structured_condition(data):
        """
        Извлекает структурированное состояние пациента из данных.
        
        Args:
            data: JSON данные документа
            
        Returns:
            dict: Структурированное состояние пациента
        """
        conditions = PatientParser.get_condition(data)
        return PatientParser.parse_conditions_as_key_value(conditions) 