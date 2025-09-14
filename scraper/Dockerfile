FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scripts and crontab template
COPY scraper_car.py scraper_queue.py scraper_functions.py crontab.template start-cron.sh ./
RUN mkdir log

# Install cron and gettext (for envsubst)
RUN apt-get update && apt-get install -y cron gettext

# Make startup script executable
RUN chmod +x start-cron.sh

# Start cron via script
CMD ["/app/start-cron.sh"]
