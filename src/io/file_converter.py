"""
Module for converting XML and JSON files.
"""
import os
import json
import xml.etree.ElementTree as ET


def xml_to_json(xml_file_path, json_file_path):
    """
    Converts XML file to JSON.
    
    Args:
        xml_file_path: Path to the XML file
        json_file_path: Path where the JSON file will be saved
    """
    # Read XML data from file
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    # Parse XML data
    root = ET.fromstring(xml_data)

    # Function to convert parsed XML element to Python dictionary
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
    """
    Processes all XML files in the specified directory and converts them to JSON.
    
    Args:
        input_directory: Input directory with XML files
        output_directory: Output directory for JSON files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Iterate through each file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".xml"):
            # Construct full paths for XML and JSON files
            path_xml = os.path.join(input_directory, filename)
            path_json = os.path.join(
                output_directory, filename.replace('.xml', '.json'))

            # Convert XML to JSON
            xml_to_json(path_xml, path_json) 