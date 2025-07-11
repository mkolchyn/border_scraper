import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from functions import get_database_connection
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

intervals = {
    "car_last_hour": "select buffer_zone_name, car_last_hour, insert_dt from buffer_zone_statistics bzs join buffer_zone bz on bz.buffer_zone_id = bzs.buffer_zone_id where bz.buffer_zone_id in (1,3);",
    "car_last_day": "select buffer_zone_name, car_last_day, insert_dt from buffer_zone_statistics bzs join buffer_zone bz on bz.buffer_zone_id = bzs.buffer_zone_id where bz.buffer_zone_id in (1,3);"
    }

conn = get_database_connection()

for interval, query in intervals.items():
    df = pd.read_sql_query(query, conn)
    df['insert_dt'] = pd.to_datetime(df['insert_dt'])
    pivot_df = df.pivot(index='insert_dt', columns='buffer_zone_name', values=interval)
    pivot_df = pivot_df.sort_index()

    plt.figure(figsize=(20, 10))
    sns.lineplot(data=pivot_df, dashes=False, markers=False)

    # Highlight days
    for i, date in enumerate(pivot_df.index):
        if date.weekday() in [5, 6]:  # Saturday and Sunday
            plt.axvspan(date, date, color='#FFC9CD', alpha=0.5)
        elif date.weekday() == 2:  # Wednesday
            plt.axvspan(date, date, color='#9AEBFF', alpha=0.5)   

    plt.title(f'Queue Length Over Time by Buffer Zone - {interval}', fontsize=30)
    plt.xticks(rotation=45, fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(fontsize=30, markerscale=1.5)
    plt.grid()
    plt.tight_layout()
    
    plt.savefig(f'{os.getenv("WORKING_DIR_PATH")}/www/sum/queue_length_visual_{interval.replace(" ", "_")}.png')
    plt.close()

conn.close()
