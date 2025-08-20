# BY to LT Border Queue Monitoring System

Hosted
[http://ec2-13-60-42-71.eu-north-1.compute.amazonaws.com/](http://ec2-13-60-196-116.eu-north-1.compute.amazonaws.com/)

## Overview

This project provides a web-based tool for visualizing historical queue lengths at border crossing points from Belarus to Lithuania. The queue data is sourced from [declarant.by](https://mon.declarant.by/zone), which reflects the number of vehicles in buffer zones over different time periods.

The system consists of a data scraper, a visualization module, and a web page.

## How It Works

### 1. Data Collection (`scraper.py`)

The `scraper.py` script collects real-time queue data from `declarant.by`. It periodically scrapes and saves this data into a database for further analysis.

### 2. Data Visualization (`visualizer.py`)

The `visualizer.py` script processes the collected data and generates graphical representations of queue lengths. These visuals include:
- Queue length for the last 3 hours
- Queue length for the last 24 hours
- Queue length for the past 7 days
- Queue length for the past 30 days

### 3. Database Schema (`DB_objects.sql`)

The `DB_objects.sql` script contains the SQL commands for setting up the database objects, including tables and necessary views to efficiently query queue data for visualization.

### 4. Web Interface (`index.html`)

The web interface provides a user-friendly way to view the generated visuals. It includes:
- A simple, clean design with flex-based layout for displaying images.
- Links to each time range of queue data.
