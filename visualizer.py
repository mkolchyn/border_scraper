import pandas as pd
import matplotlib.pyplot as plt
from scraper import get_database_connection
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

intervals = {
    "3 hours": "select * from vsl_lt_3_hrs;",
    "24 hours": "select * from vsl_lt_24_hrs;",
    "1 week": "select * from vsl_lt_1_wk;",
    "1 month": "select * from vsl_lt_1_mnth;"
    }

conn = get_database_connection()

for interval, query in intervals.items():
    
    df = pd.read_sql_query(query, conn)
    # Convert insert_dt to datetime
    df['insert_dt'] = pd.to_datetime(df['insert_dt'])
    # Pivot the DataFrame
    pivot_df = df.pivot(index='insert_dt', columns='buffer_zone_name', values='vehicle_count')
    # Sort the index to ensure correct time order
    pivot_df = pivot_df.sort_index()
    # Step 2: Plotting the Data
    plt.figure(figsize=(20, 10))
    for area in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[area], marker='o', markersize=6, label=area)

    for i, date in enumerate(pivot_df.index):
        if date.weekday() in [5, 6]:
            plt.axvspan(pivot_df.index[i], pivot_df.index[i], color='#FFC9CD', alpha=0.5)

    plt.title(f'Queue Length Over Time by Buffer Zone - {interval}', fontsize=30)
    plt.xticks(rotation=45, fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(fontsize=30, markerscale=1.5)
    plt.grid()
    plt.tight_layout()
    plt.savefig(f'{os.getenv("WORKING_DIR_PATH")}/www/queue_length_visual_{interval.replace(" ", "_")}.png')
    plt.close()

conn.close()
