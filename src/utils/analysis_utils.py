"""
Module with utilities for JSON data analysis.
"""
import os
import json
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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

def plot_value_distribution(df, title='Value distribution', num_bins=None):
    """
    Creates a chart from DataFrame with columns ["Value", "Count"].
    Supports optional binning by number of bins.

    Args:
        df (pd.DataFrame): DataFrame with 'Value' and 'Count' columns.
        title (str): Title of the chart.
        num_bins (int or None): Number of bins. If None, no binning is applied.
    """
    plt.figure(figsize=(10, 6))

    if num_bins is not None:
        min_val = df['Value'].min()
        max_val = df['Value'].max()
        bin_edges = np.linspace(min_val, max_val, num_bins + 1)

        df['Bin'] = pd.cut(df['Value'], bins=bin_edges, include_lowest=True)
        binned_df = df.groupby('Bin')['Count'].sum().reset_index()

        plt.bar(binned_df['Bin'].astype(str), binned_df['Count'])
        plt.xlabel('Value range')
        plt.title(f"{title} (binned into {num_bins} bins)")
    else:
        plt.bar(df['Value'], df['Count'])
        plt.xlabel('Value')

    plt.xticks(rotation=90, ha='right')
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