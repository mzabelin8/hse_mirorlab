"""
Utilities for working with tabular data from XML/JSON.
"""
import pandas as pd
from src.utils.helpers import clean_keys


def parse_table(json_data, prefix='{urn:hl7-org:v3}'):
    """
    Parse table from JSON data.
    
    Args:
        json_data: JSON data containing a table
        prefix: Prefix for keys in JSON
        
    Returns:
        pandas.DataFrame: Table as a DataFrame
    """
    adjusted_rows = []
    headers = [header['text'] for header in json_data[f'{prefix}table'][f'{prefix}thead'][f'{prefix}tr'][f'{prefix}th']]

    for row in json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr']:
        current_row = []
        for cell in row[f'{prefix}td']:
            current_row.append(cell[f'{prefix}content']['text'])
        # Check if the row contains fewer elements than headers, if yes, add a placeholder
        if len(current_row) < len(headers):
            current_row.append('None')
        adjusted_rows.append(current_row)

    # Create DataFrame with adjusted rows
    adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
    return adjusted_df


def parse_table_2(json_data, prefix='{urn:hl7-org:v3}'):
    """
    Parse small tables from JSON data.
    Works better with small tables.
    
    Args:
        json_data: JSON data containing a table
        prefix: Prefix for keys in JSON
        
    Returns:
        pandas.DataFrame: Table as a DataFrame
    """
    adjusted_rows = []
    headers = [header['text'] for header in json_data[f'{prefix}table'][f'{prefix}thead'][f'{prefix}tr'][f'{prefix}th']]

    # Get table rows
    rows = json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr']

    # If rows is a dictionary (one row), convert to list
    if isinstance(rows, dict):
        rows = [rows]

    # Process each row
    for row in rows:
        current_row = []
        for cell in row[f'{prefix}td']:
            # Handle cases where content may be missing or empty
            text_content = cell[f'{prefix}content'].get('text', 'None')
            current_row.append(text_content)

        # Check if the row contains fewer elements than headers, and append 'None' for missing values
        while len(current_row) < len(headers):
            current_row.append('None')

        adjusted_rows.append(current_row)

    # Create DataFrame with adjusted rows
    adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
    return adjusted_df


def parse_table_wtheader(json_data, prefix='{urn:hl7-org:v3}'):
    """
    Parse table from JSON data, automatically generating headers.
    
    Args:
        json_data: JSON data containing a table
        prefix: Prefix for keys in JSON
        
    Returns:
        pandas.DataFrame: Table as a DataFrame
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
            # Default to 'None' if 'text' is not available
            cell_text = cell[f'{prefix}content'].get('text', 'None')
            current_row.append(cell_text)
        adjusted_rows.append(current_row)

    # Create DataFrame with adjusted rows
    adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
    return adjusted_df


def convert_table_to_dataframe(table_data):
    """
    Convert tabular data to Pandas DataFrame.
    
    Args:
        table_data: Tabular data
        
    Returns:
        pandas.DataFrame: Table as a DataFrame
    """
    # Clean keys from namespace prefixes
    cleaned_data = clean_keys(table_data)

    # Extract column names from table headers
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
            # Ensure each row has the same number of columns
            if len(row_data) < len(col_names):
                row_data.extend([None]*(len(col_names) - len(row_data)))
            data_rows.append(row_data)
        elif isinstance(td, dict):
            # Handle rows with colspan (e.g., section headers)
            if 'content' in td and 'text' in td['content']:
                text = td['content']['text']
                row_data = [text] + [None]*(len(col_names)-1)
                data_rows.append(row_data)

    # Create DataFrame
    df = pd.DataFrame(data_rows, columns=col_names)
    return df


def safe_parse_table(table_data):
    """
    Attempts to parse a table using standard method, then fallback method.
    
    Args:
        table_data: Tabular data
        
    Returns:
        pandas.DataFrame: Table as a DataFrame
    """
    try:
        return convert_table_to_dataframe(table_data)
    except Exception:
        return parse_table_2(table_data)


def save_table_as_dict(table):
    """
    Converts pandas DataFrame to dictionary.
    
    Args:
        table: pandas DataFrame
        
    Returns:
        dict: Table as a dictionary
    """
    return table.to_dict(orient="list") 