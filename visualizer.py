import pandas as pd
import matplotlib.pyplot as plt
from scraper import get_database_connection
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

intervals = {
    "3 hours": "select * from visual where DATE_TRUNC('hour', insert_dt) >= DATE_TRUNC('hour', current_timestamp) - interval '3 hour';",
    "24 hours": "select * from visual where DATE_TRUNC('hour', insert_dt) >= DATE_TRUNC('hour', current_timestamp) - interval '24 hour';",
    "1 week": "select * from visual where DATE_TRUNC('hour', insert_dt) >= DATE_TRUNC('day', current_timestamp) - interval '6 day';",
    "1 month": "select * from visual where insert_dt >= DATE_TRUNC('day', current_timestamp) - interval '30 day';"
    }

conn = get_database_connection()

for interval, query in intervals.items():
    
    df = pd.read_sql_query(query, conn)
    # Convert insert_dt to datetime
    df['insert_dt'] = pd.to_datetime(df['insert_dt'])
    # Pivot the DataFrame
    pivot_df = df.pivot(index='insert_dt', columns='waiting_area_name', values='queue')
    # Sort the index to ensure correct time order
    pivot_df = pivot_df.sort_index()
    # Step 2: Plotting the Data
    plt.figure(figsize=(20, 10))
    for area in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[area], marker='o', label=area)

    plt.xlabel('Time')
    plt.ylabel('Queue Length')
    plt.title(f'Queue Length Over Time by Waiting Area - {interval}')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(f'{os.getenv("WORKING_DIR_PATH")}/www/queue_length_visual_{interval.replace(" ", "_")}.png')
    plt.close()

conn.close()
