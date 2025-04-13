"""
Модуль для конвертации XML и JSON файлов.
"""
import os
import json
import xml.etree.ElementTree as ET


class FileConverter:
    """
    Класс для конвертации файлов между форматами XML и JSON.
    """
    
    @staticmethod
    def xml_to_json(xml_file_path, json_file_path):
        """
        Конвертирует XML-файл в JSON.
        
        Args:
            xml_file_path: Путь к XML-файлу
            json_file_path: Путь, по которому будет сохранен JSON-файл
        """
        # Читаем XML-данные из файла
        with open(xml_file_path, 'r', encoding='utf-8') as file:
            xml_data = file.read()
    
        # Парсим XML-данные
        root = ET.fromstring(xml_data)
    
        # Функция для конвертации разобранного XML-элемента в Python-словарь
        def elem_to_dict(elem):
            d = {}
            for child in elem:
                if child.tag not in d:
                    d[child.tag] = elem_to_dict(child)
                else:
                    if not isinstance(d[child.tag], list):
                        d[child.tag] = [d[child.tag]]
                    d[child.tag].append(elem_to_dict(child))
            d.update({k: v for k, v in elem.attrib.items()})
            if elem.text and elem.text.strip():
                d['text'] = elem.text.strip()
            else:
                d.pop('text', None)  # Удаляем пустые текстовые поля
            return d
    
        # Конвертируем корневой элемент в словарь и сохраняем в JSON-файл
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json_data = elem_to_dict(root)
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
    
    @staticmethod
    def process_files_in_directory(input_directory, output_directory):
        """
        Обрабатывает все XML-файлы в указанной директории и конвертирует их в JSON.
        
        Args:
            input_directory: Входная директория с XML-файлами
            output_directory: Выходная директория для JSON-файлов
        """
        # Создаем выходную директорию, если она не существует
        os.makedirs(output_directory, exist_ok=True)
    
        # Перебираем каждый файл во входной директории
        for filename in os.listdir(input_directory):
            if filename.endswith(".xml"):
                # Конструируем полные пути для XML и JSON файлов
                path_xml = os.path.join(input_directory, filename)
                path_json = os.path.join(
                    output_directory, filename.replace('.xml', '.json'))
    
                # Конвертируем XML в JSON
                FileConverter.xml_to_json(path_xml, path_json) 