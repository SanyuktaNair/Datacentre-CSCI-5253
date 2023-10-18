--Q1
SELECT animal_type, count(*) FROM animal_data GROUP BY animal_type;

--Q2
SELECT COUNT(animal_id) AS "+More than 1 Outcome"
FROM (SELECT animal_id FROM outcome_events GROUP BY animal_id HAVING COUNT(*) > 1);

--Q3
SELECT
    CASE
        WHEN eMonth = 1 THEN 'January'
        WHEN eMonth = 2 THEN 'February'
        WHEN eMonth = 3 THEN 'March'
        WHEN eMonth = 4 THEN 'April'
        WHEN eMonth = 5 THEN 'May'
        WHEN eMonth = 6 THEN 'June'
        WHEN eMonth = 7 THEN 'July'
        WHEN eMonth = 8 THEN 'August'
        WHEN eMonth = 9 THEN 'September'
        WHEN eMonth = 10 THEN 'October'
        WHEN eMonth = 11 THEN 'November'
        WHEN eMonth = 12 THEN 'December'
        ELSE 'Invalid Month'
    END AS month_name,
    COUNT(*) AS month_count
FROM (SELECT EXTRACT(MONTH FROM datetime) AS eMonth FROM outcome_events) subquery
GROUP BY eMonth
ORDER BY month_count DESC
LIMIT 5;


--Q4
WITH CatAdoptions AS (
    SELECT
        a.animal_type,
        DATE_PART('year', AGE(oe.datetime, a.date_of_birth)) AS age_in_years,
        oe.outcome_type 
    FROM
        animal_data AS a
    JOIN
        outcome_events AS oe ON a.animal_id = oe.animal_id
    WHERE oe.outcome_type = 'Adoption' AND a.animal_type = 'Cat'
)

SELECT
    CASE
        WHEN age_in_years < 1 THEN 'Kitten'
        WHEN age_in_years > 10 THEN 'Senior Cat'
        ELSE 'Adult'
    END AS age_category,
    outcome_type,
    COUNT(*) AS count
FROM CatAdoptions
GROUP BY age_category;
--Q5 
SELECT
    date(datetime) AS "date",
    COUNT(*) AS "dailyOutcomes",
    SUM(COUNT(*)) OVER (ORDER BY date(datetime)) AS "Cumulative Total Outcomes"
FROM outcome_events
GROUP BY date(datetime)
ORDER BY date(datetime);
