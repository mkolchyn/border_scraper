from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import psycopg2
from psycopg2 import sql

def write_to_database(waiting_area, value_queue, value_timestamp):
    conn = psycopg2.connect(
        dbname="border_queue",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    insert_statement = sql.SQL("INSERT INTO queue (waiting_area, queue, date_src) VALUES (%s, %s, %s)")
    data = (waiting_area, value_queue, value_timestamp)
    cursor.execute(insert_statement, data)
    conn.commit()
    cursor.close()
    conn.close()


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_driver_path = "/home/kolchin/border_scraper/chromedriver-linux64/chromedriver"
chrome_service = Service(executable_path=chrome_driver_path)
chrome_driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

url = "https://belarusborder.by/"
chrome_driver.get(url=url)

element = chrome_driver.find_element(By.XPATH, "//section[@id='tablebox']/div/div/div/div/div[1]/div/div/span")
value_date = element.text
value_timestamp = datetime.strptime(value_date, "по состоянию на %H:%M | %d.%m.%Y")

element = chrome_driver.find_element(By.XPATH, "//table[@id='checkpointsTable']/tbody/tr[7]/td[2]")
value_queue = element.text.split()[0]
write_to_database(3, value_queue, value_timestamp)

element = chrome_driver.find_element(By.XPATH, "//*[@id='checkpointsTable']/tbody/tr[3]/td[2]")
value_queue = element.text.split()[0]
write_to_database(1, value_queue, value_timestamp)

element = chrome_driver.find_element(By.XPATH, "//*[@id='checkpointsTable']/tbody/tr[5]/td[2]")
value_queue = element.text.split()[0]
write_to_database(2, value_queue, value_timestamp)

chrome_driver.close()
chrome_driver.quit()
