import json
import os
import pandas as pd
import numpy as np
import re
import ast
from tqdm import tqdm

def extract_number(filename):
    """
    Extracts a numerical value from a filename
    
    Parameters:
    filename (str): The filename
    
    Returns:
    int: Numerical value or -1 if not found
    """
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else -1  # return -1 if no number is found

def filter_dataframe_by_patterns(df, column, patterns, operator='AND'):
    """
    Filters DataFrame based on a list of regex patterns (or simple strings) in the specified column
    
    Parameters:
    df (pd.DataFrame): Source DataFrame for filtering
    column (str): Column name to search for patterns
    patterns (list): List of regular expressions or simple substrings
    operator (str): 'AND' - all patterns must match simultaneously,
                   'OR' - at least one pattern should match
    
    Returns:
    tuple: Two DataFrames - (matching rows, non-matching rows)
    """
    # If the list is empty, everything matches
    if not patterns:
        return df.copy(), pd.DataFrame(columns=df.columns)
    
    # Validate operator
    op = operator.upper()
    if op not in ('AND', 'OR'):
        raise ValueError("Operator must be 'AND' or 'OR'")
    
    # Initialize mask
    mask = pd.Series(True, index=df.index) if op == 'AND' else pd.Series(False, index=df.index)
    
    for pat in patterns:
        # Always use regex=True so pattern can be either a simple string or a full regex
        contains = df[column].str.contains(pat, case=False, na=False, regex=True)
        if op == 'AND':
            mask &= contains
        else:
            mask |= contains
    
    # Split the DataFrame based on the mask and return both parts
    return df[mask], df[~mask]

def create_patients_table(folder_path, start_id=0):
    """
    Creates the main patients table from JSON files in a folder
    
    Parameters:
    folder_path (str): Path to the folder with JSON files
    start_id (int): Starting ID for patients
    
    Returns:
    pd.DataFrame: DataFrame with patient information
    """
    patients_data = []
    json_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.json')],
        key=extract_number
    )
    
    for i, file_name in enumerate(tqdm(json_files, desc="Processing patients")):
        id_patient = start_id + i
        file_path = os.path.join(folder_path, file_name)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            patient_info = {
                'id_patient': id_patient,
                'source_file': file_name,
                'sex': data.get('sex'),
                'birth_date': data.get('birth_date'),
                'type_gosp': data.get('type_gosp'),
                'way_gosp': data.get('way_gosp')
            }
            
            # Extract nested information
            if 'anamnez' in data:
                patient_info['disease_history'] = data['anamnez'].get('disease_history')
                patient_info['life_history'] = data['anamnez'].get('life_history')
            
            if 'conditions' in data:
                patient_info['condition_state'] = data['conditions'].get('Condition')
                patient_info['condition_complaints'] = data['conditions'].get('Complaints')
                patient_info['objective_status'] = data['conditions'].get('Objective status')
            
            if 'tables' in data and 'final_table1' in data['tables']:
                patient_info['disease_character'] = data['tables']['final_table1'].get('Character of the main disease')
                patient_info['hospitalization_outcome'] = data['tables']['final_table1'].get('Hospitalization outcome')
                patient_info['treatment_result'] = data['tables']['final_table1'].get('Treatment result')
                patient_info['cancer_suspicion'] = data['tables']['final_table1'].get('Suspicion of malignant neoplasm')
                patient_info['individual_post'] = data['tables']['final_table1'].get('Individual post deployment')
            
            patients_data.append(patient_info)
            
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")
    
    return pd.DataFrame(patients_data)

def create_ward_list_table(folder_path, start_entry_id=0, start_patient_id=0):
    """
    Creates the ward_list table from JSON files in a folder
    
    Parameters:
    folder_path (str): Path to the folder with JSON files
    start_entry_id (int): Starting ID for entries
    start_patient_id (int): Starting ID for patients
    
    Returns:
    pd.DataFrame: DataFrame with ward_list information
    """
    ward_list_data = []
    json_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.json')],
        key=extract_number
    )
    
    entry_id = start_entry_id
    for i, file_name in enumerate(tqdm(json_files, desc="Processing ward_list")):
        id_patient = start_patient_id + i
        file_path = os.path.join(folder_path, file_name)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'ward_list' in data:
                ward_list_df = pd.DataFrame.from_dict(data['ward_list'])
                
                # Process each non-NaN value in ward_list
                for col in ward_list_df.columns:
                    # Iterate over rows with index
                    for row_idx, value in ward_list_df[col].items():
                        if pd.notna(value):
                            ward_list_data.append({
                                'id': entry_id,
                                'id_patient': id_patient,
                                'source_file': file_name,
                                'column_name': col,
                                'row_index': row_idx,  # Use the actual DataFrame row index
                                'value': value
                            })
                            entry_id += 1
            
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")
    
    return pd.DataFrame(ward_list_data)

def create_table_generic(folder_path, table_accessor, start_table_id=0, start_patient_id=0, id_column_name='table_id'):
    """
    Universal function for creating tables from JSON files
    
    Parameters:
    folder_path (str): Path to the folder with JSON files
    table_accessor (str): Code to access the table (e.g., "pd.DataFrame.from_dict(data['tables']['table_gosp'])")
    start_table_id (int): Starting ID for the table
    start_patient_id (int): Starting ID for patients
    id_column_name (str): Column name for the table ID
    
    Returns:
    pd.DataFrame: DataFrame with combined tables
    """
    tables = []
    json_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.json')],
        key=extract_number
    )
    
    table_id = start_table_id
    for i, file_name in enumerate(tqdm(json_files, desc=f"Processing {table_accessor}")):
        id_patient = start_patient_id + i
        file_path = os.path.join(folder_path, file_name)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Get table data using eval
            locals_dict = {'pd': pd, 'data': data}
            table_df = eval(table_accessor, globals(), locals_dict)
            
            # If the table is not empty, add IDs
            if not table_df.empty:
                table_df['id_patient'] = id_patient
                table_df[id_column_name] = table_id
                table_df['source_file'] = file_name
                
                tables.append(table_df)
                table_id += 1
            
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")
    
    if tables:
        return pd.concat(tables, ignore_index=True)
    else:
        return pd.DataFrame()

def expand_table_column(df, table_column, parser_func):
    """
    Expands the DataFrame by parsing the table_column in each row
    using parser_func, and converting the resulting two-column table
    into new columns.
    
    Parameters:
    df (pd.DataFrame): Source DataFrame
    table_column (str): Name of the column in df containing data to parse
    parser_func (function): Function that takes a cell content as input
                            and returns a pd.DataFrame with two columns:
                            first - names of new columns, second - their values
    
    Returns:
    pd.DataFrame: New DataFrame obtained by concatenating df and expansion from parsed tables
    """
    parsed_rows = []
    # Process all rows with progress bar
    for idx, cell in tqdm(df[table_column].items(), total=len(df), desc="Expanding table column"):
        try:
            # First apply parse_dict_string to handle potential dictionary strings
            processed_cell = parse_dict_string(cell)
            # Then apply the parser function
            table_df = parser_func(processed_cell)
            # Extract keys and values
            keys = table_df.iloc[:, 0].astype(str).tolist()
            vals = table_df.iloc[:, 1].tolist()
            parsed_rows.append(dict(zip(keys, vals)))
        except Exception as e:
            # Empty dictionary in case of parsing error
            print(f"Error processing row {idx}: {e}")
            parsed_rows.append({})

    # Create expansion DataFrame
    expansion_df = pd.DataFrame(parsed_rows, index=df.index)

    # Concatenate along columns
    return pd.concat([df, expansion_df], axis=1)

def parse_dict_string(raw_str):
    """
    Converts a string containing a dictionary into an actual Python dict
    
    Parameters:
    raw_str (str or dict): String with content resembling a dictionary, or dictionary itself
    
    Returns:
    dict: Parsed dictionary or empty dict in case of error
    """
    # If already a dictionary, return as is
    if isinstance(raw_str, dict):
        return raw_str
        
    try:
        # Remove possible outer double quotes
        clean_str = raw_str.strip('"')
        # Convert to dictionary
        result = ast.literal_eval(clean_str)
        return result
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing string: {e}")
        return {}


        