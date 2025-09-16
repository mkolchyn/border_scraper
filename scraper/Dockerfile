FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scripts and crontab template
COPY scraper_car.py scraper_queue.py scraper_functions.py main.py ./
RUN mkdir log

# Start cron via script
CMD ["python", "main.py"]
