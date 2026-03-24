#!/usr/bin/env bash
# Restore PostgreSQL database from a backup file.
# Usage: ./scripts/restore.sh <backup_file.sql.gz>
# Optionally restore slides: ./scripts/restore.sh <db_backup> <slides_backup.tar.gz>

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <db-backup.sql.gz> [slides-backup.tar.gz]"
  exit 1
fi

DB_BACKUP="$1"
SLIDES_BACKUP="${2:-}"

if [ ! -f "$DB_BACKUP" ]; then
  echo "Error: backup file not found: $DB_BACKUP"
  exit 1
fi

echo "=== Restoring PostgreSQL from $DB_BACKUP ==="
gunzip -c "$DB_BACKUP" \
  | docker compose exec -T postgres psql -U slidev -d slidev
echo "Database restored."

if [ -n "$SLIDES_BACKUP" ] && [ -f "$SLIDES_BACKUP" ]; then
  echo "=== Restoring slides from $SLIDES_BACKUP ==="
  gunzip -c "$SLIDES_BACKUP" \
    | docker compose cp - nginx:/data/
  echo "Slides restored."
fi

echo "=== Restore complete ==="
