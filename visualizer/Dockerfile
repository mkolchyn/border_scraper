FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /visualizer

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scripts and crontab template
COPY visualizer.py visualizer_stats.py visualizer_functions.py crontab.template start-cron.sh ./

# Install cron and gettext (for envsubst)
RUN apt-get update && apt-get install -y cron gettext

# Make startup script executable
RUN chmod +x start-cron.sh

# Start cron via script
CMD ["/visualizer/start-cron.sh"]
