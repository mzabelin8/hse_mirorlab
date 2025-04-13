"""
Утилиты для работы с табличными данными из XML/JSON.
"""
import pandas as pd
from src.utils.helpers import clean_keys


def parse_table(json_data, prefix='{urn:hl7-org:v3}'):
    """
    Парсинг таблицы из JSON данных.
    
    Args:
        json_data: JSON данные, содержащие таблицу
        prefix: Префикс для ключей в JSON
        
    Returns:
        pandas.DataFrame: Таблица в виде DataFrame
    """
    adjusted_rows = []
    headers = [header['text'] for header in json_data[f'{prefix}table'][f'{prefix}thead'][f'{prefix}tr'][f'{prefix}th']]

    for row in json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr']:
        current_row = []
        for cell in row[f'{prefix}td']:
            current_row.append(cell[f'{prefix}content']['text'])
        # Проверка, содержит ли строка меньше элементов, чем заголовки, если да, добавить заполнитель
        if len(current_row) < len(headers):
            current_row.append('None')
        adjusted_rows.append(current_row)

    # Создаем DataFrame с корректированными строками
    adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
    return adjusted_df


def parse_table_2(json_data, prefix='{urn:hl7-org:v3}'):
    """
    Парсинг небольших таблиц из JSON данных.
    Лучше работает с малыми таблицами.
    
    Args:
        json_data: JSON данные, содержащие таблицу
        prefix: Префикс для ключей в JSON
        
    Returns:
        pandas.DataFrame: Таблица в виде DataFrame
    """
    adjusted_rows = []
    headers = [header['text'] for header in json_data[f'{prefix}table'][f'{prefix}thead'][f'{prefix}tr'][f'{prefix}th']]

    # Получаем строки таблицы
    rows = json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr']

    # Если rows - словарь (одна строка), конвертируем в список
    if isinstance(rows, dict):
        rows = [rows]

    # Обрабатываем каждую строку
    for row in rows:
        current_row = []
        for cell in row[f'{prefix}td']:
            # Обрабатываем случаи, когда контент может отсутствовать или быть пустым
            text_content = cell[f'{prefix}content'].get('text', 'None')
            current_row.append(text_content)

        # Проверяем, содержит ли строка меньше элементов, чем заголовки, и дополняем 'None' для отсутствующих значений
        while len(current_row) < len(headers):
            current_row.append('None')

        adjusted_rows.append(current_row)

    # Создаем DataFrame с корректированными строками
    adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
    return adjusted_df


def parse_table_wtheader(json_data, prefix='{urn:hl7-org:v3}'):
    """
    Парсинг таблицы из JSON данных, автоматически генерируя заголовки.
    
    Args:
        json_data: JSON данные, содержащие таблицу
        prefix: Префикс для ключей в JSON
        
    Returns:
        pandas.DataFrame: Таблица в виде DataFrame
    """
    adjusted_rows = []
    if json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr']:
        first_row = json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr'][0]
        num_columns = len(first_row[f'{prefix}td'])
        headers = [f'Column {i + 1}' for i in range(num_columns)]
    else:
        headers = []

    for row in json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr']:
        current_row = []
        for cell in row[f'{prefix}td']:
            # По умолчанию 'None', если 'text' недоступен
            cell_text = cell[f'{prefix}content'].get('text', 'None')
            current_row.append(cell_text)
        adjusted_rows.append(current_row)

    # Создаем DataFrame с корректированными строками
    adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
    return adjusted_df


def convert_table_to_dataframe(table_data):
    """
    Конвертация табличных данных в Pandas DataFrame.
    
    Args:
        table_data: Табличные данные
        
    Returns:
        pandas.DataFrame: Таблица в виде DataFrame
    """
    # Очищаем ключи от префиксов пространств имен
    cleaned_data = clean_keys(table_data)

    # Извлекаем имена колонок из заголовков таблицы
    headers = cleaned_data['table']['thead']['tr']['th']
    col_names = [th.get('text', None) for th in headers]

    data_rows = []
    for row in cleaned_data['table']['tbody']['tr']:
        td = row['td']
        if isinstance(td, list):
            row_data = []
            for cell in td:
                if 'text' in cell:
                    row_data.append(cell['text'])
                elif 'content' in cell and 'text' in cell['content']:
                    row_data.append(cell['content']['text'])
                else:
                    row_data.append(None)
            # Убеждаемся, что каждая строка имеет одинаковое количество столбцов
            if len(row_data) < len(col_names):
                row_data.extend([None]*(len(col_names) - len(row_data)))
            data_rows.append(row_data)
        elif isinstance(td, dict):
            # Обрабатываем строки с colspan (например, заголовки разделов)
            if 'content' in td and 'text' in td['content']:
                text = td['content']['text']
                row_data = [text] + [None]*(len(col_names)-1)
                data_rows.append(row_data)

    # Создаем DataFrame
    df = pd.DataFrame(data_rows, columns=col_names)
    return df


def safe_parse_table(table_data):
    """
    Пытается распарсить таблицу стандартным способом, затем резервным.
    
    Args:
        table_data: Табличные данные
        
    Returns:
        pandas.DataFrame: Таблица в виде DataFrame
    """
    try:
        return convert_table_to_dataframe(table_data)
    except Exception:
        return parse_table_2(table_data)


def save_table_as_dict(table):
    """
    Конвертирует pandas DataFrame в словарь.
    
    Args:
        table: pandas DataFrame
        
    Returns:
        dict: Таблица в виде словаря
    """
    return table.to_dict(orient="list") 