"""
Module for data processing and saving.
"""
import os
import json
from src.parsers.patient_parser import get_sex, get_age, get_amnez_d, get_amnez_life, get_condition, parse_conditions_as_key_value
from src.parsers.hosp_parser import get_gosp_info, get_diagnosis
from src.parsers.ward_parser import get_ward_table, compute_full_wards
from src.parsers.final_parser import get_final_table1, get_final_table2
from src.utils.table_utils import safe_parse_table, save_table_as_dict


def modify_json(in_path, out_path):
    """
    Modifies a JSON file by extracting structured data from it.
    
    Args:
        in_path: Path to the input JSON file
        out_path: Path where the result will be saved
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(in_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        result = {}

        # Extract patient data
        result['sex'] = get_sex(data)
        result['age'] = get_age(data)
        result['anamnez_d'] = get_amnez_d(data)
        result['anamnez_l'] = get_amnez_life(data)
        result['conditions'] = get_condition(data)

        # Extract hospitalization data
        table_gosp, type_gosp, way_gosp = get_gosp_info(data, type='raw')
        result['table_gosp'] = table_gosp
        result['type_gosp'] = type_gosp
        result['way_gosp'] = way_gosp
        result['diagnosis'] = get_diagnosis(data, type='raw')

        # Extract department data
        result['ward_table'] = get_ward_table(data, type='raw')
        result['ward_list'] = compute_full_wards(data)

        # Extract final tables
        result['final_table1'] = get_final_table1(data, type='raw')
        result['final_table2'] = get_final_table2(data, type='raw')

        with open(out_path, "w", encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
        
        return True
    except Exception as e:
        print(f"Error processing file {in_path}: {str(e)}")
        return False

def save_features(input_folder, output_folder):
    """
    Processes all JSON files in the specified directory and saves the extracted data.
    Handles exceptions for individual files and prints processing statistics.
    Only error messages are displayed during processing.
    
    Args:
        input_folder: Input directory with JSON files
        output_folder: Output directory for processed data
        
    Returns:
        dict: Statistics of processing (total, success, errors)
    """
    # Make sure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get a sorted list of files in the input folder
    files = sorted(f for f in os.listdir(input_folder) if f.endswith('.json'))
    
    # Counters for statistics
    total_files = len(files)
    success_count = 0
    error_count = 0

    # Process each file
    for idx, file_name in enumerate(files, start=1):
        in_path = os.path.join(input_folder, file_name)
        out_path = os.path.join(output_folder, f"file_{idx}.json")

        # Call the modify_json function with appropriate paths
        if modify_json(in_path, out_path):
            success_count += 1
        else:
            error_count += 1
    
    # Print statistics
    print(f"\nProcessing complete!")
    print(f"Total files: {total_files}")
    print(f"Successfully processed: {success_count}")
    print(f"Errors: {error_count}")
    
    return {
        "total": total_files,
        "success": success_count,
        "errors": error_count
    }

def process_data_to_structured_format(data):
    """
    Converts data to a structured format with improved organization.
    
    Args:
        data: Dictionary with data retrieved from a JSON file
        
    Returns:
        dict: Structured data format
    """
    # Convert data to a more convenient format
    processed_json = {
        "sex": data.get("sex"),
        "birth_date": data.get("age"),
        "type_gosp": data.get("type_gosp"),
        "way_gosp": data.get("way_gosp"),
        "anamnez": {
            "disease_history": data.get("anamnez_d"),
            "life_history": data.get("anamnez_l")
        },
        "conditions": parse_conditions_as_key_value(data.get("conditions", [])),
        "tables": {
            "table_gosp": save_table_as_dict(safe_parse_table(data["table_gosp"])) if data.get("table_gosp") else None,
            "diagnosis": save_table_as_dict(safe_parse_table(data["diagnosis"])) if data.get("diagnosis") else None,
            "ward_table": save_table_as_dict(safe_parse_table(data["ward_table"])) if data.get("ward_table") else None,
            "final_table1": save_table_as_dict(safe_parse_table(data["final_table1"])) if data.get("final_table1") else None,
            "final_table2": save_table_as_dict(safe_parse_table(data["final_table2"])) if data.get("final_table2") else None,
        }
    }
    
    return processed_json

def process_file_to_structured_format(in_path, out_path):
    """
    Processes a file by converting it to a structured format.
    
    Args:
        in_path: Path to the input JSON file
        out_path: Path to save the processed file
    """
    try:
        # Load data from file
        with open(in_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Apply data processing function
        processed_data = process_data_to_structured_format(data)
        
        # Save result to file
        with open(out_path, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, ensure_ascii=False, indent=4)
            
        return True
    except Exception as e:
        print(f"Error processing file {in_path}: {str(e)}")
        return False
        
def process_folder_to_structured_format(input_folder, output_folder):
    """
    Processes all files in a folder, converting them to structured format.
    Handles exceptions for individual files and prints processing statistics.
    Only error messages are displayed during processing.
    
    Args:
        input_folder: Input directory with JSON files
        output_folder: Output directory for processed files
        
    Returns:
        dict: Statistics of processing (total, success, errors)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get list of files to process
    files = [f for f in os.listdir(input_folder) if f.endswith('.json')]
    
    # Counters for statistics
    total_files = len(files)
    success_count = 0
    error_count = 0
    
    # Process each file
    for file_name in files:
        in_path = os.path.join(input_folder, file_name)
        out_path = os.path.join(output_folder, file_name)
        
        if process_file_to_structured_format(in_path, out_path):
            success_count += 1
        else:
            error_count += 1
    
    # Print statistics
    print(f"\nProcessing complete!")
    print(f"Total files: {total_files}")
    print(f"Successfully processed: {success_count}")
    print(f"Errors: {error_count}")
    
    return {
        "total": total_files,
        "success": success_count,
        "errors": error_count
    } 