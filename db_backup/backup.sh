#!/bin/bash
set -e

DATE=$(date +"%Y%m%d_%H%M%S")

# Make sure backup dir exists
mkdir -p "/backups"

# Run pg_dump
pg_dump "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}" \
  | gzip > "/backups/${DB_NAME}_${DATE}.sql.gz"

# Optional: remove old backups (keep last 7 days)
find "/backups" -type f -mtime +7 -delete
