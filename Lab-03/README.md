# Lab 03: Airflow

## Assignment
In this lab, we'll schedule the pipeline with Airflow

Create an Airflow DAG that:

- Starts on November 1 2023
- Runs daily
- Retrieves current data from Austin Animal Shelter Outcomes data source (though the API or csv)
    - You cannot use shelter1000.csv for this lab
- Transforms the data into the dimensional data model
    - Every independent transformation should be its own task, e.
- Loads the data into data warehouse
    - Loading of a single table should be its own task
    - There should not be duplicates, e.g. duplicate animals


Things to consider:
- Retrive the entire file or just the data for the necessary date?
- Drop all the existing data and rewrite it, or append/update existing records?


## Folder structure

The `Setup` folder contains the solution to Lab 02 that we'll use as a starting point