"""
Module with utilities for JSON data analysis.
"""
import os
import json
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

def analyze_json_values(directory, value_expression):
    """
    Extracts values from JSON files and returns a DataFrame with their distribution.

    Args:
        directory (str): Path to directory with JSON files.
        value_expression (str): Python expression to extract value from the `data` variable.

    Returns:
        pd.DataFrame: Table with columns ["Value", "Count"].
    """
    value_counts = Counter()
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

    for filename in tqdm(json_files, desc="Processing files"):
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                value = eval(value_expression)
                value_counts[value] += 1
        except Exception as e:
            print(f"Error in file {filename}: {e}")

    df = pd.DataFrame(value_counts.items(), columns=['Value', 'Count']).sort_values(by='Count', ascending=False)
    return df

def plot_value_distribution(df, title='Value distribution'):
    """
    Creates a chart from DataFrame with columns ["Value", "Count"].

    Args:
        df (pd.DataFrame): Value table.
        title (str): Chart title.
    """
    plt.figure(figsize=(8, 5))
    plt.bar(df['Value'], df['Count'])
    plt.xticks(rotation=90, ha='right')
    plt.title(title)
    plt.xlabel('Value')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()

def find_files_with_value(directory, value_expression, target_value):
    """
    Returns a list of files where the value from the eval expression equals the target value.

    Args:
        directory (str): Path to directory with JSON files.
        value_expression (str): Python expression to extract value from the `data` variable.
        target_value (any): Value to find.

    Returns:
        list of str: Filenames where the value matches.
    """
    matching_files = []
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

    for filename in tqdm(json_files, desc="Searching files"):
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                value = eval(value_expression)
                if value == target_value:
                    matching_files.append(filename)
        except Exception as e:
            print(f"Error in file {filename}: {e}")

    return matching_files 