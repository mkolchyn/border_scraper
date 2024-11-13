import os
from dotenv import load_dotenv
import psycopg2
import requests

# Load environment variables from .env file
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


def fetch_data_from_api(url):
    """Fetch JSON data from the provided API."""
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")


def insert_data_into_qla(buffer_zone_id, data):
    """Insert fetched data into the border_statistics table."""
    query = """
    INSERT INTO queue_length_all (
    	buffer_zone_id, count_all, count_car, count_truck, count_bus, count_motorcycle, count_live_queue, count_bookings,
        count_priority, count_passed_scc
    ) VALUES (
    %(buffer_zone_id)s, %(countAll)s, %(countCar)s, %(countTruck)s, %(countBus)s, %(countMotorcycle)s, %(countLiveQueue)s,
    %(countBookings)s, %(countPriority)s, %(countPassedSCC)s
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


def insert_data_into_bzs(buffer_zone_id, data):
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