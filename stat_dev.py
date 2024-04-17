from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import psycopg2
from psycopg2 import sql
import time

def write_to_database(waiting_area, passed_last_hour, passed_last_24h):
    conn = psycopg2.connect(
        dbname="border_queue",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    insert_statement = sql.SQL("INSERT INTO queue_stat (waiting_area, passed_last_hour, passed_last_24h) VALUES (%s, %s, %s)")
    data = (waiting_area, passed_last_hour, passed_last_24h)
    cursor.execute(insert_statement, data)
    conn.commit()
    cursor.close()
    conn.close()

chrome_options = Options()
chrome_options.add_argument("--headless")

chrome_driver_path = "D:\\EPAM-Data_Engineering\\Training\\LAB\\LAB_2_DWH ETL PostgreSQL\\Part_5_DQE\\Topic_12\\hw\\chromedriver\\chromedriver.exe"
chrome_service = Service(executable_path=chrome_driver_path)
chrome_driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

url = "https://mon.declarant.by/zone/kamennii-log"
chrome_driver.get(url=url)
time.sleep(5)

element = chrome_driver.find_element(By.XPATH, "/html/body/app-root/div/div/app-zone-detail/div/app-customs-card/div/app-vehicles-table/app-zone-statistics/div/div/p[1]/span")
passed_last_hour = element.text.split()[0]
element = chrome_driver.find_element(By.XPATH, "/html/body/app-root/div/div/app-zone-detail/div/app-customs-card/div/app-vehicles-table/app-zone-statistics/div/div/p[2]/span")
passed_last_24h = element.text.split()[0]
write_to_database(3, passed_last_hour, passed_last_24h)


chrome_driver.close()
chrome_driver.quit()