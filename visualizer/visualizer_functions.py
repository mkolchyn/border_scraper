import os
from dotenv import load_dotenv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

def create_visual (intervals, cln_index, cln_columns, cln_values):
    
    conn = get_database_connection()

    for interval, query in intervals.items():
        
        df = pd.read_sql_query(query, conn)
        df[cln_index] = pd.to_datetime(df[cln_index])
        pivot_df = df.pivot(index=cln_index, columns=cln_columns, values=cln_values)
        pivot_df = pivot_df.sort_index()
        
        plt.figure(figsize=(20, 10))
        sns.lineplot(data=pivot_df, dashes=False, markers=False)
        
        # Highlight days
        for i, date in enumerate(pivot_df.index):
            if date.weekday() in [5, 6]:  # Saturday and Sunday
                plt.axvspan(date, date, color='#FFC9CD', alpha=0.5)
            elif date.weekday() == 2:  # Wednesday
                plt.axvspan(date, date, color='#9AEBFF', alpha=0.5)   

        # Annotate values on the plot
        for line in pivot_df.columns:
            for x, y in zip(pivot_df.index, pivot_df[line]):
                if not pd.isna(y):
                    plt.text(x, y, f'{y:.2f}', color='black', fontsize=20, ha='center', va='bottom')

        plt.title(f'Queue Length Over Time by Buffer Zone - {interval}', fontsize=30)
        plt.xticks(rotation=45, fontsize=20)
        plt.yticks(fontsize=20)
        plt.legend(fontsize=20)
        plt.grid()
        plt.tight_layout()
        
        plt.savefig(f'./www/queue_length_visual_{interval.replace(" ", "_")}.png')
        plt.close()

    conn.close()