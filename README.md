# Docker and SQL Homework

## Question 1: Understanding Docker First Run

### Overview
the goal is to run a docker container using python 3.12.8 image in interactive mode, using `bash` shell as the entry point

### steps to solve 

1. pulled the python image (python: 3.12.8) and run the image interactively with the following command
-
```bash
docker run it --entrypoint bash python:3.12.8
```
2. **Check `pip` version**
  - run the following command inside the container
  ```bash
      pip  --version 
  ```
  - output: 
  ```
  pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)

  ```
### output
**Answer** the version of `pip` in the `python:3.12.8` image is **24.3.1**

## Question 2: understanding Docker Networking and Docker Compose

### Overview
This task involves understanding how docker compose services communicate within the same network. 

### Analysis of `docker-compose.yaml`

1. **Host and port for pgAdmin:**
   -**Hostname:** `db`
   -**port:** `5432`

### Test the setup with the following steps
1. save the `docker-compose.yaml` file. 
2. Run the following command: 
    ```bash
        docker-compose up 
    ```
### Importing Green Taxi Data
 1. Downloaded all the csv files
 2. created `load_data.py` file with all the necessary instructions to import data
 3. create a `Dockerfile` for the load_data.py
 4. updated the `docker-compose.yaml` file to include the `load_data` container

 ## Question 3 Trip Segmentation Count

 The following SQL query calculates the number of trips during the period of October 1st, 2019 (inclusive) to November 1st, 2019 (exclusive), segmented by trip distance:

- **Up to 1 mile**
- **Between 1 (exclusive) and 3 miles (inclusive)**
- **Between 3 (exclusive) and 7 miles (inclusive)**
- **Between 7 (exclusive) and 10 miles (inclusive)**
- **Over 10 miles**
```sql
SELECT
    SUM(CASE WHEN trip_distance <= 1 THEN 1 ELSE 0 END) AS up_to_1_mile,
    SUM(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 ELSE 0 END) AS between_1_and_3_miles,
    SUM(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 ELSE 0 END) AS between_3_and_7_miles,
    SUM(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 ELSE 0 END) AS between_7_and_10_miles,
    SUM(CASE WHEN trip_distance > 10 THEN 1 ELSE 0 END) AS over_10_miles
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01'
  AND lpep_pickup_datetime < '2019-11-01'
  AND lpep_dropoff_datetime < '2019-11-01';
```
- **The Answer is** `104,802; 198,924; 109,603; 27,678; 35,189`

## Question 4. Longest trip for each day

### SQL Query:
```sql
select 
Date(lpep_pickup_datetime) As trip_date,
Max(trip_distance) as max_trip_distance

from public.green_taxi_trips

GROUP BY trip_date
ORDER BY max_trip_distance desc;
```
-**The Answer is** `2019-10-31`

## Question 5. Three biggest pickup zones

### SQL Query: 

```sql
SELECT 
    b."Zone", 
    SUM(a.total_amount) AS total_amount 
FROM public.green_taxi_trips a
INNER JOIN public.taxi_zones b 
    ON a."PULocationID" = b."LocationID"
WHERE CAST(a.lpep_pickup_datetime AS DATE) = '2019-10-18'  -- Filter by the specific date
GROUP BY b."Zone" 
HAVING SUM(a.total_amount) > 13000  -- Only consider zones with a total amount over 13,000
ORDER BY total_amount DESC  -- Sort in descending order by total amount
LIMIT 3;  -- Return only the top 3 pickup zones
```
-**The Zones are**: `East Harlem North, East Harlem South, Morningside Heights`

## Question 6. Largest tip: 

### SQL QUERY

``` SQL
-- Select the drop-off zone with the largest tip for passengers picked up from "East Harlem North" in October 2019
SELECT 
    d."Zone",  -- Retrieve the drop-off zone name
    c.LargestTip  -- Retrieve the largest tip for the respective drop-off zone
FROM (
    -- Subquery to calculate the largest tip for each drop-off zone for trips picked up in "East Harlem North" in October 2019
    SELECT 
        a."DOLocationID",  -- Drop-off location ID
        MAX(a.tip_amount) AS LargestTip  -- Find the maximum tip amount for each drop-off zone
    FROM public.green_taxi_trips a
    INNER JOIN public.taxi_zones b 
        ON a."PULocationID" = b."LocationID"  -- Join with taxi_zones table to filter by pickup zone
    WHERE CAST(a.lpep_pickup_datetime AS DATE) >= '2019-10-01' 
      AND CAST(a.lpep_pickup_datetime AS DATE) <= '2019-10-31'  -- Filter trips in October 2019
      AND b."Zone" = 'East Harlem North'  -- Only consider trips picked up in "East Harlem North"
    GROUP BY a."DOLocationID"  -- Group by drop-off location ID to calculate the largest tip for each drop-off zone
) c 
INNER JOIN public.taxi_zones d 
    ON c."DOLocationID" = d."LocationID"  -- Join the subquery result with taxi_zones to get the drop-off zone name
ORDER BY c.LargestTip DESC  -- Sort the results by the largest tip in descending order
LIMIT 1;  -- Limit the result to return only the drop-off zone with the largest tip
```
-**The drop-off zone with the largest tip was:** `JFK Airport`