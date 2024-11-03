import os
from dotenv import load_dotenv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
from psycopg2 import sql


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


def write_to_database(cursor, waiting_area, value_queue, value_timestamp):
    """Insert data into the database."""
    insert_statement = sql.SQL("INSERT INTO queue (waiting_area, queue, date_src) VALUES (%s, %s, %s)")
    data = (waiting_area, value_queue, value_timestamp)
    cursor.execute(insert_statement, data)


def get_element_text(driver, xpath):
    """Retrieve the text of a web element identified by its XPATH."""
    element = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    return element.text


def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
    chrome_service = Service(executable_path=chrome_driver_path)
    chrome_driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        chrome_driver.get(url="https://mon.declarant.by/zone")
        # Retrieve date information
        value_date = get_element_text(chrome_driver, "//html/body/app-root/div/div/app-zone-list/div/div/div")
        value_timestamp = datetime.strptime(value_date, "По состоянию на: %d.%m.%Y | %H:%M")

        # Define the waiting area xpaths
        xpaths = {
            1: "/html/body/app-root/div/div/app-zone-list/div/div/app-customs-card/div/app-customs-table/div/table/tbody/tr[1]/td[1]",
            2: "/html/body/app-root/div/div/app-zone-list/div/div/app-customs-card/div/app-customs-table/div/table/tbody/tr[3]/td[1]",
            3: "/html/body/app-root/div/div/app-zone-list/div/div/app-customs-card/div/app-customs-table/div/table/tbody/tr[5]/td[1]",
            4: "/html/body/app-root/div/div/app-zone-list/div/div/app-customs-card/div/app-customs-table/div/table/tbody/tr[4]/td[1]",
        }

        # Open a single database connection
        connection = get_database_connection()
        cursor = connection.cursor()

        # Iterate through the xpaths and write to the database
        for waiting_area, xpath in xpaths.items():
            value_queue = get_element_text(chrome_driver, xpath)
            write_to_database(cursor, waiting_area, value_queue, value_timestamp)

        connection.commit()  # Commit once after all inserts
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        chrome_driver.quit()


if __name__ == "__main__":
    main()
