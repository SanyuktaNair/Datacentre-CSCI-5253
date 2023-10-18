#!/usr/bin/env python
# coding: utf-8

import sys
import pandas as pd
import numpy as np
import argparse
from sqlalchemy import create_engine

def extract_data(source):
    df = pd.read_csv(source)
    return df

def transform_data(data):
    print('Transforming data...')
    # Your transformation logic here
    data_new = data.copy()
    data_new.fillna('Not Recorded', inplace=True)
    data_new.columns = [col.lower() for col in data_new.columns]
    animal_columns = ['animal_id', 'breed', 'color', 'name', 'date_of_birth', 'animal_type']
    outcome_event_columns = ['outcome_event_id', 'datetime', 'sex_upon_outcome', 'outcome_subtype', 'animal_id', 'outcome_type_id']
    fact_table_columns = ['outcome_event_id', 'outcome_type_id', 'animal_id']

    data_new['outcome_event_id'] = range(1, len(data_new) + 1)

    animal = data_new[animal_columns].drop_duplicates('animal_id', keep='first').reset_index(drop=True)
    
    unique_outcome_type = data_new[['outcome_type']].drop_duplicates().reset_index(drop=True)
    unique_outcome_type['outcome_type_id'] = unique_outcome_type.index + 1
    outcome_type = unique_outcome_type[['outcome_type_id', 'outcome_type']]
    outcome_type_id_map = dict(zip(unique_outcome_type['outcome_type'], unique_outcome_type['outcome_type_id']))
    data_new['outcome_type_id'] = data_new['outcome_type'].map(outcome_type_id_map)

    outcome_events = data_new[outcome_event_columns]
    
    outcome_events.reset_index(drop=True, inplace=True)
    fact_table = data_new[fact_table_columns]
    print('Data Transformed')
    return fact_table, animal, outcome_type, outcome_events
    
def load_data(transformed_data):        
    fact_table, animal, outcome_type, outcome_events = transformed_data
    engine = create_engine(DATABASE_URL)       
    outcome_events.to_sql('outcome_events', engine, if_exists='append', index=False)
    fact_table.to_sql('fact_table', engine, if_exists='append', index=False)
    animal.to_sql('animal', engine, if_exists='append', index=False) 
    outcome_type.to_sql('outcome_type', engine, if_exists='append', index=False)
    print('Data Loading Completed')

if __name__ == '__main':    
    source = sys.argv[1]
    extracted_data = extract_data(source)
    transformed_data = transform_data(extracted_data)
    load_data(transformed_data) 