import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import psycopg2

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


def insert_data_into_db(buffer_zone_id, query, data):
    """Insert fetched data into the border_statistics table."""
    
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


def convert_date(date_str):
    return datetime.strptime(date_str, "%H:%M:%S %d.%m.%Y")