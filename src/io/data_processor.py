"""
Модуль для обработки и сохранения данных.
"""
import os
import json
from src.parsers.patient_parser import PatientParser
from src.parsers.hosp_parser import HospParser
from src.parsers.ward_parser import WardParser
from src.parsers.final_parser import FinalParser
from src.utils.table_utils import safe_parse_table, save_table_as_dict


class DataProcessor:
    """
    Класс для обработки и сохранения данных из JSON-файлов.
    """
    
    @staticmethod
    def modify_json(in_path, out_path):
        """
        Модифицирует JSON-файл, извлекая из него структурированные данные.
        
        Args:
            in_path: Путь к входному JSON-файлу
            out_path: Путь, по которому будет сохранен результат
        """
        with open(in_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    
        result = {}
    
        # Извлечение данных о пациенте
        result['sex'] = PatientParser.get_sex(data)
        result['age'] = PatientParser.get_age(data)
        result['anamnez_d'] = PatientParser.get_amnez_d(data)
        result['anamnez_l'] = PatientParser.get_amnez_life(data)
        result['conditions'] = PatientParser.get_condition(data)
    
        # Извлечение данных о госпитализации
        table_gosp, type_gosp, way_gosp = HospParser.get_gosp_info(data, type='raw')
        result['table_gosp'] = table_gosp
        result['type_gosp'] = type_gosp
        result['way_gosp'] = way_gosp
        result['diagnosis'] = HospParser.get_diagnosis(data, type='raw')
    
        # Извлечение данных об отделениях
        result['ward_table'] = WardParser.get_ward_table(data, type='raw')
        result['ward_list'] = WardParser.compute_full_wards(data)
    
        # Извлечение финальных таблиц
        result['final_table1'] = FinalParser.get_final_table1(data, type='raw')
        result['final_table2'] = FinalParser.get_final_table2(data, type='raw')
    
        with open(out_path, "w", encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
    
    @staticmethod
    def save_features(input_folder, output_folder):
        """
        Обрабатывает все JSON-файлы в указанной директории и сохраняет извлеченные данные.
        
        Args:
            input_folder: Входная директория с JSON-файлами
            output_folder: Выходная директория для обработанных данных
        """
        # Проверяем, что выходная папка существует
        os.makedirs(output_folder, exist_ok=True)
    
        # Получаем отсортированный список файлов во входной папке
        files = sorted(f for f in os.listdir(input_folder) if f.endswith('.json'))
    
        # Обрабатываем каждый файл
        for idx, file_name in enumerate(files, start=1):
            in_path = os.path.join(input_folder, file_name)
            out_path = os.path.join(output_folder, f"file_{idx}.json")
    
            # Вызываем функцию modify_json с соответствующими путями
            DataProcessor.modify_json(in_path, out_path)
    
    @staticmethod
    def process_data_to_structured_format(data):
        """
        Преобразует данные в структурированный формат с улучшенной организацией.
        
        Args:
            data: Словарь с данными, полученными из JSON-файла
            
        Returns:
            dict: Структурированный формат данных
        """
        # Преобразуем данные в более удобный формат
        processed_json = {
            "sex": data.get("sex"),
            "birth_date": data.get("age"),
            "type_gosp": data.get("type_gosp"),
            "way_gosp": data.get("way_gosp"),
            "anamnez": {
                "disease_history": data.get("anamnez_d"),
                "life_history": data.get("anamnez_l")
            },
            "conditions": PatientParser.parse_conditions_as_key_value(data.get("conditions", [])),
            "tables": {
                "table_gosp": save_table_as_dict(safe_parse_table(data["table_gosp"])) if data.get("table_gosp") else None,
                "diagnosis": save_table_as_dict(safe_parse_table(data["diagnosis"])) if data.get("diagnosis") else None,
                "ward_table": save_table_as_dict(safe_parse_table(data["ward_table"])) if data.get("ward_table") else None,
                "final_table1": save_table_as_dict(safe_parse_table(data["final_table1"])) if data.get("final_table1") else None,
                "final_table2": save_table_as_dict(safe_parse_table(data["final_table2"])) if data.get("final_table2") else None,
            }
        }
        
        return processed_json
    
    @staticmethod
    def process_file_to_structured_format(in_path, out_path):
        """
        Обрабатывает файл, преобразуя его в структурированный формат.
        
        Args:
            in_path: Путь к входному JSON-файлу
            out_path: Путь для сохранения обработанного файла
        """
        try:
            # Загружаем данные из файла
            with open(in_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Применяем функцию обработки данных
            processed_data = DataProcessor.process_data_to_structured_format(data)
            
            # Сохраняем результат в файл
            with open(out_path, 'w', encoding='utf-8') as file:
                json.dump(processed_data, file, ensure_ascii=False, indent=4)
                
            return True
        except Exception as e:
            print(f"Ошибка обработки файла {in_path}: {str(e)}")
            return False
            
    @staticmethod
    def process_folder_to_structured_format(input_folder, output_folder):
        """
        Обрабатывает все файлы в папке, преобразуя их в структурированный формат.
        
        Args:
            input_folder: Входная директория с JSON-файлами
            output_folder: Выходная директория для обработанных файлов
        """
        # Создаем выходную директорию, если она не существует
        os.makedirs(output_folder, exist_ok=True)
        
        # Получаем список файлов для обработки
        files = [f for f in os.listdir(input_folder) if f.endswith('.json')]
        
        # Счетчики для статистики
        success_count = 0
        error_count = 0
        
        # Обрабатываем каждый файл
        for file_name in files:
            in_path = os.path.join(input_folder, file_name)
            out_path = os.path.join(output_folder, file_name)
            
            if DataProcessor.process_file_to_structured_format(in_path, out_path):
                success_count += 1
            else:
                error_count += 1
                
        return {
            "total": len(files),
            "success": success_count,
            "errors": error_count
        } 