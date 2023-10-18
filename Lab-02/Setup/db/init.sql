CREATE TABLE fact_table (
    animal_id VARCHAR(50) NOT NULL,
    outcome_type_id INT,
    outcome_event_id INT,
    FOREIGN KEY (animal_id) REFERENCES animal(animal_id),
    FOREIGN KEY (outcome_type_id) REFERENCES outcome_type(outcome_type_id),
    FOREIGN KEY (outcome_event_id) REFERENCES outcome_events(outcome_event_id) 
);

CREATE TABLE outcome_type (
    outcome_type_id INT PRIMARY KEY,
    outcome_type VARCHAR(50)
);

CREATE TABLE outcome_events (
    outcome_event_id INT PRIMARY KEY,
    datetime TIMESTAMP,
    sex_upon_outcome VARCHAR(50),
    outcome_subtype VARCHAR(50),
    animal_id VARCHAR(50),
    FOREIGN KEY (outcome_type_id) REFERENCES outcome_type(outcome_type_id),
    FOREIGN KEY (animal_id) REFERENCES animal(animal_id),
    FOREIGN KEY (outcome_type_id) REFERENCES outcome_type(outcome_type_id)
);

CREATE TABLE animal (
    animal_id VARCHAR(50) PRIMARY KEY,
    breed VARCHAR(50),
    color VARCHAR(50),
    name VARCHAR(50),
    date_of_birth DATE,
    animal_type VARCHAR(50)
);