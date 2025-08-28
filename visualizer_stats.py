import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from functions import get_database_connection
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

intervals = {
    "cars_per_hour": "select * from cars_per_hour_last_day;",
    "cars_per_day": "select * from cars_per_day_last_7_days;"
    }

conn = get_database_connection()

for interval, query in intervals.items():
    df = pd.read_sql_query(query, conn)
    df['dt'] = pd.to_datetime(df['dt'], utc=True).dt.tz_convert('Europe/Minsk')
    pivot_df = df.pivot(index='dt', columns='buffer_zone_name', values=interval)
    pivot_df = pivot_df.sort_index()

    plt.figure(figsize=(20, 10))
    sns.lineplot(data=pivot_df, dashes=False, markers=False)

    # Always start Y-axis at 0
    plt.ylim(bottom=0)

    # Hide axis names
    plt.xlabel("")
    plt.ylabel("")

    # Highlight days
    for i, date in enumerate(pivot_df.index):
        if date.weekday() in [5, 6]:  # Saturday and Sunday
            plt.axvspan(date, date, color='#FFC9CD', alpha=0.5)
        elif date.weekday() == 2:  # Wednesday
            plt.axvspan(date, date, color='#9AEBFF', alpha=0.5)   

    plt.title(f'The number of cars that passed through the Buffer Zone - {interval}', fontsize=30)
    plt.xticks(rotation=45, fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(fontsize=30, markerscale=1.5)
    plt.grid()
    plt.tight_layout()
    
    plt.savefig(f'{os.getenv("WORKING_DIR_PATH")}/www/sum/queue_length_visual_{interval.replace(" ", "_")}.png')
    plt.close()

conn.close()
