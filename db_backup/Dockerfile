FROM postgres:16

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy script
COPY backup.sh /usr/local/bin/backup.sh
RUN chmod +x /usr/local/bin/backup.sh

# Cron job (every day at 2 AM)
RUN echo "0 2 * * * root . /etc/environment && /usr/local/bin/backup.sh >> /var/log/cron.log 2>&1" \
    > /etc/cron.d/pg_backup


# Apply cron permissions
RUN chmod 0644 /etc/cron.d/pg_backup && crontab /etc/cron.d/pg_backup

CMD ["cron", "-f"]
