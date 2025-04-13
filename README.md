# Парсер Медицинских Данных

Библиотека для парсинга и извлечения структурированной информации из медицинских XML/JSON документов.

## Структура Проекта

```
src/
├── __init__.py
├── main.py                  # Главный модуль с основными функциями
├── io/                      # Модуль работы с файлами
│   ├── __init__.py
│   ├── file_converter.py    # Конвертация XML в JSON
│   └── data_processor.py    # Обработка и сохранение данных
├── parsers/                 # Модуль с парсерами
│   ├── __init__.py
│   ├── base_parser.py       # Базовый класс для парсеров
│   ├── patient_parser.py    # Парсер данных пациента
│   ├── hosp_parser.py       # Парсер данных о госпитализации
│   ├── ward_parser.py       # Парсер данных об отделениях
│   ├── final_parser.py      # Парсер финальных таблиц
│   └── lab_parser.py        # Парсер лабораторных данных
└── utils/                   # Утилиты
    ├── __init__.py
    ├── helpers.py           # Вспомогательные функции
    └── table_utils.py       # Функции для работы с таблицами
```

## Примеры использования

### Конвертация XML файла в JSON

```python
from src.main import convert_xml_to_json

convert_xml_to_json('path/to/file.xml', 'path/to/output.json')
```

### Обработка всех XML файлов в директории

```python
from src.main import process_directory

process_directory('input_directory', 'output_directory')
```

### Извлечение структурированных данных из JSON

```python
from src.main import process_json_data

process_json_data('path/to/json_file.json', 'path/to/output.json')
```

### Использование отдельных парсеров

```python
import json
from src.main import patient_parser, hosp_parser

# Загрузка данных
with open('path/to/json_file.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Извлечение пола пациента
sex = patient_parser.get_sex(data)

# Извлечение информации о госпитализации
table, type_gosp, way_gosp = hosp_parser.get_gosp_info(data)
```

## Обработка всех файлов

Для обработки всех файлов в директории и сохранения результатов:

```python
from src.main import process_all_json_files

process_all_json_files('input_json_directory', 'output_features_directory')
```

