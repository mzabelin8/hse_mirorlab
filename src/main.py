"""
Главный модуль для удобного доступа к основным функциям парсинга.
"""
from src.io.file_converter import FileConverter
from src.io.data_processor import DataProcessor
from src.parsers.patient_parser import PatientParser
from src.parsers.hosp_parser import HospParser
from src.parsers.ward_parser import WardParser
from src.parsers.final_parser import FinalParser
from src.parsers.lab_parser import LabParser
from src.utils.table_utils import safe_parse_table, save_table_as_dict


def convert_xml_to_json(xml_path, json_path):
    """
    Конвертирует XML-файл в JSON-формат.
    
    Args:
        xml_path: Путь к XML-файлу
        json_path: Путь для сохранения JSON-файла
    """
    FileConverter.xml_to_json(xml_path, json_path)
    
    
def process_directory(input_dir, output_dir):
    """
    Обрабатывает все XML-файлы в директории.
    
    Args:
        input_dir: Входная директория с XML-файлами
        output_dir: Выходная директория для JSON-файлов
    """
    FileConverter.process_files_in_directory(input_dir, output_dir)
    
    
def process_json_data(json_path, output_path):
    """
    Обрабатывает один JSON-файл и сохраняет структурированные данные.
    
    Args:
        json_path: Путь к исходному JSON-файлу
        output_path: Путь для сохранения результатов
    """
    DataProcessor.modify_json(json_path, output_path)
    
    
def process_all_json_files(input_dir, output_dir):
    """
    Обрабатывает все JSON-файлы в директории.
    
    Args:
        input_dir: Входная директория с JSON-файлами
        output_dir: Выходная директория для обработанных данных
    """
    DataProcessor.save_features(input_dir, output_dir)


def process_data_to_structured_format(data):
    """
    Преобразует данные в структурированный формат с улучшенной организацией.
    
    Args:
        data: Словарь с данными, полученными из JSON-файла
        
    Returns:
        dict: Структурированный формат данных
    """
    return DataProcessor.process_data_to_structured_format(data)


def process_file_to_structured_format(in_path, out_path):
    """
    Обрабатывает файл, преобразуя его в структурированный формат.
    
    Args:
        in_path: Путь к входному JSON-файлу
        out_path: Путь для сохранения обработанного файла
        
    Returns:
        bool: True в случае успеха, False в случае ошибки
    """
    return DataProcessor.process_file_to_structured_format(in_path, out_path)


def process_folder_to_structured_format(input_folder, output_folder):
    """
    Обрабатывает все файлы в папке, преобразуя их в структурированный формат.
    
    Args:
        input_folder: Входная директория с JSON-файлами
        output_folder: Выходная директория для обработанных файлов
        
    Returns:
        dict: Статистика обработки (total, success, errors)
    """
    return DataProcessor.process_folder_to_structured_format(input_folder, output_folder)


# Экспортируем утилитные функции для прямого использования
def parse_conditions_as_key_value(conditions):
    """
    Парсит каждую строку условия как 'ключ: значение', если возможно.
    """
    return PatientParser.parse_conditions_as_key_value(conditions)


# Экспортируем все парсеры для прямого использования
# Например: from src.main import patient_parser
patient_parser = PatientParser
hosp_parser = HospParser
ward_parser = WardParser
final_parser = FinalParser
lab_parser = LabParser 