import pandas as pd
import xml.etree.ElementTree as ET
from io import StringIO
import json
import os

from src.parser_main import *


def xml_to_json(xml_file_path, json_file_path):
    # Read XML data from file
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Function to convert the parsed XML element into a Python dictionary
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
            d.pop('text', None)  # Remove empty text fields
        return d

    # Convert the root element to a dictionary and save to JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_data = elem_to_dict(root)
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)


def process_files_in_directory(input_directory, output_directory):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Iterate through each file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".xml"):
            # Construct the full paths for the XML and JSON files
            path_xml = os.path.join(input_directory, filename)
            path_json = os.path.join(
                output_directory, filename.replace('.xml', '.json'))

            # Convert XML to JSON
            xml_to_json(path_xml, path_json)

            # Open the generated JSON file and read its content
            with open(path_json, 'r', encoding='utf-8') as file:
                data = json.load(file)


def modify_json(in_path, out_path):
    with open(in_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    result = {}

    sex = get_sex(data)
    result['sex'] = sex

    age = get_age(data)
    result['age'] = age

    table_gosp, type_gosp, way_gosp = get_gosp_info(data, type='raw')
    result['table_gosp'] = table_gosp
    result['type_gosp'] = type_gosp
    result['way_gosp'] = way_gosp

    diagnosis = get_diagnosis(data, type='raw')
    result['diagnosis'] = diagnosis

    anamnez_d = get_amnez_d(data)
    result['anamnez_d'] = anamnez_d

    anamnez_l = get_amnez_life(data)
    result['anamnez_l'] = anamnez_l

    conditions = get_condition(data)
    result['conditions'] = conditions

    ward_table = get_ward_table(data, type='raw')
    result['ward_table'] = ward_table

    ward_list = compute_full_wards(data)
    result['ward_list'] = ward_list

    final_table1 = get_final_table1(data, type='raw')
    result['final_table1'] = final_table1

    final_table2 = get_final_table2(data, type='raw')
    result['final_table2'] = final_table2

    with open(out_path, "w", encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)


def save_features(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get a sorted list of files in the input folder
    files = sorted(f for f in os.listdir(input_folder) if f.endswith('.json'))

    # Process each file
    for idx, file_name in enumerate(files, start=1):
        in_path = os.path.join(input_folder, file_name)
        out_path = os.path.join(output_folder, f"file_{idx}.json")

        # Call the modify_json function with the appropriate paths
        modify_json(in_path, out_path)
