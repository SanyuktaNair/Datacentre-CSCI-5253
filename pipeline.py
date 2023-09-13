import pandas as pd
import numpy as np
import argparse

def extract_data(source):
  return pd.read_csv(source)

def transform_data(data):
  new_data = data.copy()
  new_data['Content'] = new_data['Content Rating'].replace(["Unrated"],["Everyone"])
  new_data['Updated date'] = pd.to_datetime(new_data['Last Updated'], format='%d/%m/%Y', errors='coerce')
  new_data.drop(columns = ['Size','Content Rating','Last Updated'], inplace=True)
  return new_data

def load_data(data, target):
  data.to_csv(target)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='source csv')
    parser.add_argument('target', help='target csv')
    args = parser.parse_args()

    print("Starting.{}..".format(args.source))
    df = extract_data(args.source)
    new_df = transform_data(df)
    load_data(new_df, args.target)
    print("Complete")