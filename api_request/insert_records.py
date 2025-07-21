import psycopg2
from datetime import datetime, timezone
from api_request import fetch_data

def connect_to_db():
    print("Connecting to the PostgreSQL database...")
    try:
        conn = psycopg2.connect(
            host="host.docker.internal",
            port=5432,
            dbname="weatherstack",  # You might want to rename this to "openweather"
            user="airflow",
            password="airflow"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise

def create_table(conn):
    print("Creating table if not exists...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                country TEXT,
                temperature FLOAT,
                feels_like FLOAT,
                weather_description TEXT,
                weather_main TEXT,
                wind_speed FLOAT,
                wind_degree INTEGER,
                humidity INTEGER,
                pressure INTEGER,
                visibility INTEGER,
                cloudiness INTEGER,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset INTEGER,
                sunrise TIMESTAMP,
                sunset TIMESTAMP,
                latitude FLOAT,
                longitude FLOAT
            );
        """)
        conn.commit()
        print("Table was created.")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise

def insert_records(conn, data_list):
    print("Inserting weather data into the database...")
    
    # Check if data_list is actually a list
    if not isinstance(data_list, list):
        print("Error: Expected a list of weather data, but received a single object")
        return
    
    inserted_count = 0
    cursor = conn.cursor()
    
    for data in data_list:
        try:
            # Extract data from OpenWeatherMap format
            city = data['name']
            country = data['sys']['country']
            temperature = data['main']['temp']
            feels_like = data['main']['feels_like']
            weather_description = data['weather'][0]['description']
            weather_main = data['weather'][0]['main']
            wind_speed = data['wind']['speed']  # m/s
            wind_degree = data['wind'].get('deg', 0)
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            visibility = data.get('visibility', 0) // 1000  # Convert m to km
            cloudiness = data['clouds']['all']
            
            # Convert timestamps
            current_time = datetime.fromtimestamp(data['dt'], tz=timezone.utc)
            sunrise = datetime.fromtimestamp(data['sys']['sunrise'], tz=timezone.utc)
            sunset = datetime.fromtimestamp(data['sys']['sunset'], tz=timezone.utc)
            utc_offset = data['timezone']  # seconds from UTC
            
            # Coordinates
            latitude = data['coord']['lat']
            longitude = data['coord']['lon']
            
            cursor.execute("""
                INSERT INTO dev.raw_weather_data (
                    city,
                    country,
                    temperature,
                    feels_like,
                    weather_description,
                    weather_main,
                    wind_speed,
                    wind_degree,
                    humidity,
                    pressure,
                    visibility,
                    cloudiness,
                    time,
                    inserted_at,
                    utc_offset,
                    sunrise,
                    sunset,
                    latitude,
                    longitude
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s)
            """, (
                city,
                country,
                temperature,
                feels_like,
                weather_description,
                weather_main,
                wind_speed,
                wind_degree,
                humidity,
                pressure,
                visibility,
                cloudiness,
                current_time,
                utc_offset,
                sunrise,
                sunset,
                latitude,
                longitude
            ))
            
            inserted_count += 1
            print(f"✓ Data inserted for {city}, {country}")
            
        except psycopg2.Error as e:
            print(f"✗ Database error inserting data for {data.get('name', 'Unknown')}: {e}")
            continue
        except KeyError as e:
            print(f"✗ Missing field {e} in API response for {data.get('name', 'Unknown')}")
            continue
        except Exception as e:
            print(f"✗ Unexpected error inserting data for {data.get('name', 'Unknown')}: {e}")
            continue
    
    # Commit all insertions at once
    try:
        conn.commit()
        print(f"Successfully inserted data for {inserted_count} cities.")
    except psycopg2.Error as e:
        print(f"Error committing transaction: {e}")
        conn.rollback()
        raise

def main():
    try:
        data = fetch_data()
        conn = connect_to_db()
        create_table(conn)
        
        # Choose which insert function to use:
        insert_records(conn, data)  # Full version with all OpenWeatherMap fields
        #insert_records_simple(conn, data)  # Simplified version matching original structure
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")

# if __name__ == "__main__":
#     main()