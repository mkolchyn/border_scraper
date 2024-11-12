import requests
import psycopg2
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_database_connection():
    """Create a database connection using credentials from a .env file."""
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def fetch_data_from_api(checkpointId):
    """Fetch JSON data from the provided API."""
    url = f'https://belarusborder.by/info/monitoring/statistics?token=test&checkpointId={checkpointId}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

def insert_data_into_db(buffer_zone_id, data):
    """Insert fetched data into the border_statistics table."""
    query = """
    INSERT INTO buffer_zone_statistics (
        buffer_zone_id, native_id, checkpoint_id, car_last_hour, motorcycle_last_hour, truck_last_hour, 
        bus_last_hour, car_last_day, truck_last_day, bus_last_day, motorcycle_last_day
    ) VALUES (
        %(buffer_zone_id)s, %(id)s, %(checkpointId)s, %(carLastHour)s, %(motorcycleLastHour)s, %(truckLastHour)s, 
        %(busLastHour)s, %(carLastDay)s, %(truckLastDay)s, %(busLastDay)s, %(motorcycleLastDay)s
    )
    """
    
    # Add buffer_zone_id to the data dictionary
    data['buffer_zone_id'] = buffer_zone_id
    
    conn = None
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, data)
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def main():
    """Main function to orchestrate data fetching and insertion."""
    try:
        scope = {
            1: "53d94097-2b34-11ec-8467-ac1f6bf889c0",
            2: "a9173a85-3fc0-424c-84f0-defa632481e4",
            3: "b60677d4-8a00-4f93-a781-e129e1692a03",
            4: "ffe81c11-00d6-11e8-a967-b0dd44bde851",
        }

        for buffer_zone_id, checkpointId in scope.items():
            data = fetch_data_from_api(checkpointId)  # Pass only checkpointId
            insert_data_into_db(buffer_zone_id, data)  # Pass buffer_zone_id and data
            print(f"Data for buffer_zone_id {buffer_zone_id} inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
