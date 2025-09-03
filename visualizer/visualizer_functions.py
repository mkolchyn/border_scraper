import os
from dotenv import load_dotenv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()

def get_database_connection():
    """Create a database connection using SQLAlchemy."""
    db_url = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    engine = create_engine(db_url)
    return engine

def create_visual (intervals, cln_index, cln_columns, cln_values):
    
    conn = get_database_connection()

    for country, interval, query in intervals:
        df = pd.read_sql_query(query, conn)
        df[cln_index] = pd.to_datetime(df[cln_index], utc=True).dt.tz_convert(ZoneInfo(os.getenv('TZ')))
        pivot_df = df.pivot(index=cln_index, columns=cln_columns, values=cln_values)
        pivot_df = pivot_df.sort_index()

        plt.figure(figsize=(20, 10))
        sns.lineplot(data=pivot_df, dashes=False, markers=False)

        # Highlight weekends and Wednesdays
        for date in pivot_df.index:
            if date.weekday() in [5, 6]:  # Sat/Sun
                plt.axvspan(date, date, color='#FFC9CD', alpha=0.5)
            elif date.weekday() == 2:  # Wednesday
                plt.axvspan(date, date, color='#9AEBFF', alpha=0.5)

        # Hide axis names
        plt.xlabel("")
        plt.ylabel("")

        plt.title(f'Queue Length in {country} Over Time by Buffer Zone - {interval}', fontsize=30)
        plt.xticks(rotation=45, fontsize=20)
        plt.yticks(fontsize=20)

        # Add legend including creation date
        creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        plt.plot([], [], ' ', label=f"Created on: {creation_date}")  # invisible dummy plot
        plt.legend(fontsize=20, loc="upper right")

        plt.grid()
        plt.tight_layout()

        # Save figure
        plt.savefig(f'/visualizer/www/{country}/queue_length_visual_{interval.replace(" ", "_")}.png')
        plt.close()

    conn.dispose()
