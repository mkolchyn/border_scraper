#!/bin/bash
set -e

BACKUP_DIR="/backups"
LATEST_BACKUP=$(ls -1t "$BACKUP_DIR"/*.sql.gz 2>/dev/null | head -n 1)

# Wait until Postgres is ready to accept connections
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; do
    echo "Waiting for postgres to be ready..."
    sleep 2
done

if [ -n "$LATEST_BACKUP" ]; then
    echo ">>> Found backup: $LATEST_BACKUP"
    echo ">>> Restoring into database: $POSTGRES_DB"
    gunzip -c "$LATEST_BACKUP" | psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
    echo ">>> Restore finished. Skipping schema initialization."
    # Prevent execution of *.sql files (since restore already handled schema + data)
    mv /docker-entrypoint-initdb.d/*.sql /tmp/ 2>/dev/null || true
else
    echo ">>> No backup found, proceeding with schema initialization."
    # Leave .sql files in place → they’ll run automatically
fi
