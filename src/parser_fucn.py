import pandas as pd


def find_section_by_optimized_path(data, short_path, fields=None, prefix='{urn:hl7-org:v3}'):
    """
    Navigate a nested JSON structure along the specified path, automatically adding a prefix to string path elements.
    Optionally return only specific fields from the final block.

    :param data: The JSON data as a nested Python dictionary.
    :param short_path: The simplified path to the desired section as a list of keys and indices.
    :param fields: Optional. A tuple or list of field names to return from the final block. If None, returns the entire block.
    :param prefix: The prefix to add to string elements in the path.
    :return: The section at the specified path, or specific fields from the section, or None if the path is invalid.
    """
    current = data
    full_path = [(prefix + element) if isinstance(element, str)
                 else element for element in short_path]

    try:
        for key in full_path:
            if isinstance(current, list):  # Handle list indices
                current = current[int(key)]
            else:  # Handle dictionary keys
                current = current[key]

        if fields and isinstance(fields, (list, tuple)) and isinstance(current, dict):
            return {field: current.get(field, None) for field in fields}

        return current
    except (KeyError, IndexError, ValueError, TypeError):
        return None  # Path was invalid


def parse_table(json_data, prefix='{urn:hl7-org:v3}'):
    adjusted_rows = []
    headers = [header['text'] for header in json_data[f'{prefix}table'][f'{prefix}thead'][f'{prefix}tr'][f'{prefix}th']]

    for row in json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr']:
        current_row = []
        for cell in row[f'{prefix}td']:
            current_row.append(cell[f'{prefix}content']['text'])
        # Check if the row has fewer items than headers, if so, add a placeholder
        if len(current_row) < len(headers):
            # Assuming 'Not specified' for missing doctor data
            current_row.append('None')
        adjusted_rows.append(current_row)

    # Recreate the DataFrame with adjusted rows
    adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
    return adjusted_df


def parse_table_2(json_data, prefix='{urn:hl7-org:v3}'):
    """
    For small tables works better.
    """

    adjusted_rows = []
    headers = [header['text'] for header in json_data[f'{prefix}table'][f'{prefix}thead'][f'{prefix}tr'][f'{prefix}th']]

    # Get the table rows
    rows = json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr']

    # If rows is a dictionary (single row), convert it to a list
    if isinstance(rows, dict):
        rows = [rows]

    # Process each row
    for row in rows:
        current_row = []
        for cell in row[f'{prefix}td']:
            # Handle cases where content might be missing or empty
            text_content = cell[f'{prefix}content'].get('text', 'None')
            current_row.append(text_content)

        # Check if the row has fewer items than headers, and pad with 'None' for missing values
        while len(current_row) < len(headers):
            current_row.append('None')  # Assuming 'None' for missing data

        adjusted_rows.append(current_row)

    # Recreate the DataFrame with adjusted rows
    adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
    return adjusted_df


def parse_table_wtheader(json_data, prefix='{urn:hl7-org:v3}'):
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

    # Recreate the DataFrame with adjusted rows
    adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
    return adjusted_df


def clean_keys(obj):
    """Recursively remove namespace prefixes from dictionary keys."""
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


def convert_table_to_dataframe(table_data):
    """Convert the given table data into a Pandas DataFrame."""
    # Clean the keys to remove namespace prefixes
    cleaned_data = clean_keys(table_data)

    # Extract column names from the table headers
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

    # Create the DataFrame

    df = pd.DataFrame(data_rows, columns=col_names)
    return df
