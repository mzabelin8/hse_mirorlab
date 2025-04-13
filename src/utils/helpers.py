"""
Вспомогательные функции для работы с данными.
"""
import pandas as pd


def find_section_by_optimized_path(data, short_path, fields=None, prefix='{urn:hl7-org:v3}'):
    """
    Навигация по вложенной структуре JSON по указанному пути, автоматически добавляя префикс к строковым элементам пути.
    Опционально возвращает только указанные поля из конечного блока.

    Args:
        data: Данные JSON в виде вложенного словаря Python.
        short_path: Упрощенный путь к нужному разделу в виде списка ключей и индексов.
        fields: Опционально. Кортеж или список имен полей для возврата из конечного блока. 
                Если None, возвращает весь блок.
        prefix: Префикс, добавляемый к строковым элементам пути.
    
    Returns:
        Раздел по указанному пути, или конкретные поля из раздела, или None, если путь недействителен.
    """
    current = data
    full_path = [(prefix + element) if isinstance(element, str)
                 else element for element in short_path]

    try:
        for key in full_path:
            if isinstance(current, list):  # Обработка индексов списка
                current = current[int(key)]
            else:  # Обработка ключей словаря
                current = current[key]

        if fields and isinstance(fields, (list, tuple)) and isinstance(current, dict):
            return {field: current.get(field, None) for field in fields}

        return current
    except (KeyError, IndexError, ValueError, TypeError):
        return None  # Путь недействителен


def clean_keys(obj):
    """
    Рекурсивно удаляет префиксы пространств имен из ключей словаря.
    
    Args:
        obj: Объект (словарь, список или скаляр) для обработки
        
    Returns:
        Объект с очищенными ключами
    """
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            new_key = key
            if key.startswith('{'):
                new_key = key[key.find('}')+1:]
            new_dict[new_key] = clean_keys(value)
        return new_dict
    elif isinstance(obj, list):
        return [clean_keys(item) for item in obj]
    else:
        return obj 