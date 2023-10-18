#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def extract_data():
    print("Data Extraction in Progress")
    data = pd.read_json('https://data.austintexas.gov/resource/9t4d-g238.json')
    print("Data Extracted!..")
    return data


def transform_data(data):
    print("Data Transformation in progress.....")
    # Your transformation logic here
    data_new = data.copy()
    data_new.fillna('Not Recorded', inplace=True)
    data_new.columns = [col.lower() for col in data_new.columns]

    # Define the columns for each entity
    animal_columns = ['animal_id', 'name', 'date_of_birth', 'animal_type', 'breed_id']
    outcome_event_columns = ['outcome_event_id', 'datetime', 'animal_id', 'outcome_type']
    fact_table_columns = ['outcome_event_id', 'animal_id', 'breed_id']

    

 # Create a unique outcome_event_id
    data_new['outcome_event_id'] = data_new.index + 1  
    

    outcome_events = data_new[outcome_event_columns]

    unique_breed_type = data_new[['breed']].drop_duplicates().reset_index(drop=True)
    unique_breed_type['breed_id'] = unique_breed_type.index + 1
    breed_type = unique_breed_type[['breed_id', 'breed']]

    breed_type_id_map = dict(zip(unique_breed_type['breed'], unique_breed_type['breed_id']))
    data_new['breed_id'] = data_new['breed'].map(breed_type_id_map)

    # Correct duplication for 'animal' and 'outcome_type' tables
    animal_data = data_new[animal_columns].drop_duplicates().reset_index(drop=True)
    

    # Reset the index of outcome_events DataFrame
    outcome_events.reset_index(drop=True, inplace=True)

    fact_table = data_new[fact_table_columns]
    print('Data Transformed!')
    return fact_table, animal_data, outcome_events, breed_type



from sqlalchemy.exc import IntegrityError

def load_data(transformed_data):
    print('Loading data...')
    
    fact_table, animal_data, outcome_events, breed_type = transformed_data

    # Define your DATABASE_URL here

    DATABASE_URL = "postgresql+psycopg2://sanyukta:sanyu123@db:5432/shelter"

    engine = create_engine(DATABASE_URL)   

    animal_data.to_sql('animal_data', engine, if_exists='append', index=False) 

    breed_type.to_sql('breed_type', engine, if_exists='append', index=False)
 
    outcome_events.to_sql('outcome_events', engine, if_exists='append', index=False)
   
    fact_table.to_sql('fact_table', engine, if_exists='append', index=False)
 
    
    print('Data Loading Completed')


if __name__ == '__main__':
    # Extract data
    extracted_data = extract_data()
    
    # Transform data
    transformed_data = transform_data(extracted_data)
    
    # Load data
    load_data(transformed_data)
