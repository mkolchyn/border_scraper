import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from functions import get_database_connection, create_visual
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
    df['insert_dt'] = pd.to_datetime(df['insert_dt'])
    pivot_df = df.pivot(index='insert_dt', columns='buffer_zone_name', values='count_car')
    pivot_df = pivot_df.sort_index()
    
    plt.figure(figsize=(20, 10))
    sns.lineplot(data=pivot_df, dashes=False, markers=False)

    # Hide axis names
    plt.xlabel("")
    plt.ylabel("")
    
    # Highlight days
    for i, date in enumerate(pivot_df.index):
        if date.weekday() in [5, 6]:  # Saturday and Sunday
            plt.axvspan(date, date, color='#FFC9CD', alpha=0.5)
        elif date.weekday() == 2:  # Wednesday
            plt.axvspan(date, date, color='#9AEBFF', alpha=0.5)   

    plt.title(f'Queue Length Over Time by Buffer Zone - {interval}', fontsize=30)
    plt.xticks(rotation=45, fontsize=20)
    plt.yticks(fontsize=20)
    plt.legend(fontsize=20)
    plt.grid()
    plt.tight_layout()
    
    plt.savefig(f'{os.getenv("WORKING_DIR_PATH")}/www/queue_length_visual_{interval.replace(" ", "_")}.png')
    plt.close()

conn.close()



intervals = {
    "car_origin_ratio":"select * from vsl_all_car_origin_ratio vacor order by insert_dt;"
}

create_visual(intervals, 'insert_dt', 'buffer_zone_name', 'ratio_BY_to_other')
