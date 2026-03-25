#!/usr/bin/env bash
# Backup PostgreSQL database and slide files.
# Usage: ./scripts/backup.sh [backup_dir] [compose_file] [env_file]
# Defaults: ./backups, docker-compose.prod.yml, .env.production
# Keeps 7 days of backups.

set -euo pipefail

BACKUP_DIR="${1:-./backups}"
COMPOSE_FILE="${2:-docker-compose.prod.yml}"
ENV_FILE="${3:-.env.production}"
RETENTION_DAYS=7
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

COMPOSE_CMD="docker compose --env-file $ENV_FILE -f $COMPOSE_FILE"

mkdir -p "$BACKUP_DIR"

echo "=== Backing up PostgreSQL ==="
$COMPOSE_CMD exec -T postgres pg_dump -U slidev slidev \
  | gzip > "$BACKUP_DIR/db-$TIMESTAMP.sql.gz"
echo "Saved: $BACKUP_DIR/db-$TIMESTAMP.sql.gz"

echo "=== Backing up slides ==="
$COMPOSE_CMD cp nginx:/data/slides - \
  | gzip > "$BACKUP_DIR/slides-$TIMESTAMP.tar.gz"
echo "Saved: $BACKUP_DIR/slides-$TIMESTAMP.tar.gz"

echo "=== Cleaning backups older than $RETENTION_DAYS days ==="
find "$BACKUP_DIR" -name "db-*.sql.gz" -mtime +$RETENTION_DAYS -delete -print
find "$BACKUP_DIR" -name "slides-*.tar.gz" -mtime +$RETENTION_DAYS -delete -print

echo "=== Backup complete ==="
