#!/usr/bin/env bash
# Backup PostgreSQL database and optionally slide files.
# Usage: ./scripts/backup.sh [backup_dir]
# Default backup dir: ./backups
# Keeps 7 days of backups.

set -euo pipefail

BACKUP_DIR="${1:-./backups}"
RETENTION_DAYS=7
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "=== Backing up PostgreSQL ==="
docker compose exec -T postgres pg_dump -U slidev slidev \
  | gzip > "$BACKUP_DIR/db-$TIMESTAMP.sql.gz"
echo "Saved: $BACKUP_DIR/db-$TIMESTAMP.sql.gz"

echo "=== Backing up slides ==="
docker compose cp nginx:/data/slides - \
  | gzip > "$BACKUP_DIR/slides-$TIMESTAMP.tar.gz"
echo "Saved: $BACKUP_DIR/slides-$TIMESTAMP.tar.gz"

echo "=== Cleaning backups older than $RETENTION_DAYS days ==="
find "$BACKUP_DIR" -name "db-*.sql.gz" -mtime +$RETENTION_DAYS -delete -print
find "$BACKUP_DIR" -name "slides-*.tar.gz" -mtime +$RETENTION_DAYS -delete -print

echo "=== Backup complete ==="
