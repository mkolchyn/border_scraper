import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from visualizer_functions import create_visual
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

intervals = [
    ("lithuania", "3 hours", "select * from vsl_lt_3_hrs;"),
    ("lithuania", "24 hours", "select * from vsl_lt_24_hrs;"),
    ("lithuania", "1 week", "select * from vsl_lt_1_wk;"),
    ("lithuania", "1 month", "select * from vsl_lt_1_mnth;"),
    ("latvia", "3 hours", "select * from vsl_lv_3_hrs;"),
    ("latvia", "24 hours", "select * from vsl_lv_24_hrs;"),
    ("latvia", "1 week", "select * from vsl_lv_1_wk;"),
    ("latvia", "1 month", "select * from vsl_lv_1_mnth;"),
    ("poland", "3 hours", "select * from vsl_pl_3_hrs;"),
    ("poland", "24 hours", "select * from vsl_pl_24_hrs;"),
    ("poland", "1 week", "select * from vsl_pl_1_wk;"),
    ("poland", "1 month", "select * from vsl_pl_1_mnth;")
]

create_visual(intervals, 'insert_dt', 'buffer_zone_name', 'count_car')
