#!/bin/bash
set -euo pipefail

# 1) Export the container env so cron jobs can see DB_* etc.
#    Use 'export KEY=VALUE' lines so it's safe to 'source'.
printenv | sed 's/^\([^=]*\)=\(.*\)$/export \1=\2/' > /app/container.env

# 2) Render the cron file by replacing variables in template
envsubst < /app/crontab.template > /etc/cron.d/border_scraper_cron

# 3) Correct permissions & ensure logs exist
chmod 0644 /etc/cron.d/border_scraper_cron
touch /var/log/scraper_car.log /var/log/scraper_queue.log

# 4) Run cron in the foreground for Docker
cron -f
