#!/usr/bin/env bash
# Restore PostgreSQL database from a backup file.
# Usage: ./scripts/restore.sh <db-backup.sql.gz> [slides-backup.tar.gz] [compose_file] [env_file]

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <db-backup.sql.gz> [slides-backup.tar.gz] [compose_file] [env_file]"
  exit 1
fi

DB_BACKUP="$1"
SLIDES_BACKUP="${2:-}"
COMPOSE_FILE="${3:-docker-compose.prod.yml}"
ENV_FILE="${4:-.env.production}"

COMPOSE_CMD="docker compose --env-file $ENV_FILE -f $COMPOSE_FILE"

if [ ! -f "$DB_BACKUP" ]; then
  echo "Error: backup file not found: $DB_BACKUP"
  exit 1
fi

echo "=== Restoring PostgreSQL from $DB_BACKUP ==="
gunzip -c "$DB_BACKUP" \
  | $COMPOSE_CMD exec -T postgres psql -U slidev -d slidev
echo "Database restored."

if [ -n "$SLIDES_BACKUP" ] && [ -f "$SLIDES_BACKUP" ]; then
  echo "=== Restoring slides from $SLIDES_BACKUP ==="
  gunzip -c "$SLIDES_BACKUP" \
    | $COMPOSE_CMD cp - nginx:/data/
  echo "Slides restored."
fi

echo "=== Restarting mcp-server ==="
$COMPOSE_CMD restart mcp-server

echo "=== Restore complete ==="
