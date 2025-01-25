import time
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData
from sqlalchemy.exc import OperationalError

def load_data_to_postgres():
    # Database connection parameters
    postgres_user = "postgres"
    postgres_password = "postgres"
    postgres_db = "ny_taxi"
    postgres_host = "db"  # Docker service name
    postgres_port = "5432"

    # Retry mechanism for connecting to the database
    max_retries = 10  # Number of retries
    retries = 0
    while retries < max_retries:
        try:
            # Create SQLAlchemy engine and connection
            engine = create_engine(f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}")
            connection = engine.connect()
            print("Successfully connected to the database")
            break  # Exit loop if connection is successful
        except OperationalError:
            retries += 1
            print(f"Attempt {retries} of {max_retries}: Database not ready, retrying in 5 seconds...")
            time.sleep(5)  # Wait before retrying
    else:
        print("Error: Unable to connect to the database after multiple attempts.")
        return

    metadata = MetaData()

    # Define table schema explicitly
    trips_table = Table(
        'green_taxi_trips', metadata,
        Column('VendorID', Integer),
        Column('lpep_pickup_datetime', String),
        Column('lpep_dropoff_datetime', String),
        Column('store_and_fwd_flag', String),
        Column('RatecodeID', Integer),
        Column('PULocationID', Integer),
        Column('DOLocationID', Integer),
        Column('passenger_count', Integer),
        Column('trip_distance', Float),
        Column('fare_amount', Float),
        Column('extra', Float),
        Column('mta_tax', Float),
        Column('tip_amount', Float),
        Column('tolls_amount', Float),
        Column('ehail_fee', Float, nullable=True),
        Column('improvement_surcharge', Float),
        Column('total_amount', Float),
        Column('payment_type', Integer),
        Column('trip_type', Integer),
        Column('congestion_surcharge', Float, nullable=True)
    )

    # Create table if it doesn't exist
    metadata.create_all(engine)

    # Load and clean trips CSV data
    trips_file = "green_tripdata_2019-10.csv"
    df_trips = pd.read_csv(trips_file)

    # Standardize column names and map to the table schema
    df_trips.columns = [col.strip() for col in df_trips.columns]  # Strip extra spaces
    required_columns = ['VendorID', 'lpep_pickup_datetime', 'lpep_dropoff_datetime', 'store_and_fwd_flag',
                        'RatecodeID', 'PULocationID', 'DOLocationID', 'passenger_count', 'trip_distance',
                        'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'ehail_fee',
                        'improvement_surcharge', 'total_amount', 'payment_type', 'trip_type',
                        'congestion_surcharge']
    df_trips = df_trips[required_columns]

    # Fill NaN values to avoid issues during insertion (adjust default values if needed)
    fill_values = {
        'VendorID': 0,
        'RatecodeID': 0,
        'passenger_count': 0,
        'trip_distance': 0.0,
        'fare_amount': 0.0,
        'extra': 0.0,
        'mta_tax': 0.0,
        'tip_amount': 0.0,
        'tolls_amount': 0.0,
        'ehail_fee': 0.0,
        'improvement_surcharge': 0.0,
        'total_amount': 0.0,
        'payment_type': 0,
        'trip_type': 0,
        'congestion_surcharge': 0.0
    }
    df_trips.fillna(fill_values, inplace=True)

    # Insert trips data into the database
    try:
        df_trips.to_sql('green_taxi_trips', con=engine, if_exists='append', index=False)
        print(f"Successfully inserted {len(df_trips)} rows into 'green_taxi_trips'.")
    except Exception as e:
        print(f"Error inserting trips data: {e}")

    # Load and insert zones data (if necessary)
    try:
        zones_file = "taxi_zone_lookup.csv"
        df_zones = pd.read_csv(zones_file)
        df_zones.to_sql('taxi_zones', con=engine, if_exists='append', index=False)
        print(f"Successfully inserted {len(df_zones)} rows into 'taxi_zones'.")
    except Exception as e:
        print(f"Error inserting zones data: {e}")

if __name__ == "__main__":
    load_data_to_postgres()
