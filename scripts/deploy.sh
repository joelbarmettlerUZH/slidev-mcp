#!/bin/bash
set -euo pipefail

# Deploy latest images to production server.
# Usage: DEPLOY_HOST=your-vm.example.com ./scripts/deploy.sh

REMOTE_HOST="${DEPLOY_HOST:?Set DEPLOY_HOST env var}"
REMOTE_USER="${DEPLOY_USER:-ubuntu}"
REMOTE_DIR="${DEPLOY_DIR:-/opt/slidev-mcp}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Deploying to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}"

# Ensure remote directory structure exists
echo "Ensuring remote directory structure..."
ssh "${REMOTE_USER}@${REMOTE_HOST}" "mkdir -p ${REMOTE_DIR}/docker ${REMOTE_DIR}/scripts"

# Sync compose file, nginx config, and helper scripts
echo "Syncing configuration files..."
scp -q \
  "$PROJECT_ROOT/docker-compose.prod.yml" \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/"

scp -q \
  "$PROJECT_ROOT/docker/nginx.conf" \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/docker/"

scp -q \
  "$PROJECT_ROOT/scripts/backup.sh" \
  "$PROJECT_ROOT/scripts/restore.sh" \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/scripts/"

ssh "${REMOTE_USER}@${REMOTE_HOST}" <<COMMANDS
  set -euo pipefail
  cd "${REMOTE_DIR}"
  docker compose --env-file .env.production -f docker-compose.prod.yml pull
  docker compose --env-file .env.production -f docker-compose.prod.yml up -d --remove-orphans
  docker image prune -f
  echo "Deploy complete. Services:"
  docker compose --env-file .env.production -f docker-compose.prod.yml ps --format "table {{.Name}}\t{{.Status}}"
COMMANDS
