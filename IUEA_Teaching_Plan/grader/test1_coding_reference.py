"""Lecturer reference implementation. Excluded from student packets."""
import pandas as pd
import matplotlib.pyplot as plt

def explore_data(input_records):
    observation_data = pd.DataFrame(input_records)
    return {'preview': observation_data.head(), 'rows': len(observation_data),
            'columns': len(observation_data.columns),
            'missing': observation_data.isna().sum(),
            'duplicates': observation_data.duplicated('record_id').sum()}

def plot_observations(input_records, target_unit, chart_title):
    observation_data = pd.DataFrame(input_records)
    figure, axes = plt.subplots()
    axes.scatter(observation_data['load_pct'], observation_data['target'])
    axes.set_title(chart_title)
    axes.set_xlabel('Load (%)')
    axes.set_ylabel('Target (' + target_unit + ')')
    return figure

def clean_observations(input_records):
    observation_data = pd.DataFrame(input_records)
    cleaned_data = observation_data.drop_duplicates('record_id').copy()
    rows_to_keep = cleaned_data['target'].notna() & cleaned_data['load_pct'].between(0,100)
    cleaned_data = cleaned_data[rows_to_keep].copy()
    cleaned_data['ambient_c'] = cleaned_data['ambient_c'].fillna(cleaned_data['ambient_c'].median())
    return cleaned_data

def plot_cleaned(input_records, target_unit, chart_title):
    return plot_observations(input_records, target_unit, chart_title)

def calculate_statistics(input_records):
    cleaned_data = pd.DataFrame(input_records)
    return {'mean': cleaned_data['target'].mean(), 'sum': cleaned_data['target'].sum(),
            'median': cleaned_data['target'].median(), 'count': cleaned_data['target'].count(),
            'std': cleaned_data['target'].std(), 'mode': cleaned_data['equipment_id'].mode().tolist()}

def summarize_equipment(input_records):
    cleaned_data = pd.DataFrame(input_records)
    return cleaned_data.groupby('equipment_id')['target'].agg(['mean','sum','count'])

def classify_load(load_pct):
    if load_pct < 40:
        return 'low'
    elif load_pct <= 75:
        return 'medium'
    else:
        return 'high'

def count_load_bands(load_values):
    counts = {'low': 0, 'medium': 0, 'high': 0}
    for load_pct in load_values:
        band = classify_load(load_pct)
        counts[band] += 1
    return counts
