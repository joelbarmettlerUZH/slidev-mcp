#!/bin/bash
set -euo pipefail

# Provision a new Slidev MCP server on Infomaniak OpenStack.
# Repeatable: run again with a different name to add nodes.
#
# Prerequisites:
#   - OpenStack CLI installed (pip install python-openstackclient)
#   - OS_* environment variables set (source your openrc file or .env)
#   - SSH key at ~/.ssh/slidev-mcp-infomaniak (created by first run if missing)
#
# Usage:
#   ./scripts/provision.sh <server-name> <domain>
#
# Example:
#   ./scripts/provision.sh slidev-mcp-server slidev-mcp.org

SERVER_NAME="${1:?Usage: provision.sh <server-name> <domain>}"
DOMAIN="${2:?Usage: provision.sh <server-name> <domain>}"

# Verify OpenStack auth early
AUTH_OK=0
openstack token issue -f value -c id &>/dev/null && AUTH_OK=1
if [ "$AUTH_OK" -ne 1 ]; then
    echo "[ERROR] OpenStack authentication failed. Ensure OS_* env vars are set."
    echo "  Tip: source your openrc file, or run with env prefix."
    exit 1
fi

# ---------------------------------------------------------------------------
# Configuration — change these if needed
# ---------------------------------------------------------------------------
FLAVOR="a4-ram8-disk50-perf1"
IMAGE="Ubuntu 24.04 LTS Noble Numbat"
NETWORK="ext-net1"
SECGROUP="slidev-mcp"
KEYPAIR="slidev-mcp-key"
SSH_KEY_PATH="$HOME/.ssh/slidev-mcp-infomaniak"
SSH_USER="ubuntu"  # Default user for Ubuntu cloud images

# Docker images (from GHCR)
GHCR_REPO="ghcr.io/joelbarmettleruzh/slidev-mcp"

echo "=== Slidev MCP Server Provisioning ==="
echo "  Server:  $SERVER_NAME"
echo "  Domain:  $DOMAIN"
echo "  Flavor:  $FLAVOR"
echo "  Image:   $IMAGE"
echo ""

# ---------------------------------------------------------------------------
# Step 1: Ensure SSH keypair exists locally and in OpenStack
# ---------------------------------------------------------------------------
if [ ! -f "$SSH_KEY_PATH" ]; then
    echo "[1/6] Generating SSH keypair..."
    ssh-keygen -t ed25519 -f "$SSH_KEY_PATH" -N "" -C "slidev-mcp-deploy"
fi

if openstack keypair show "$KEYPAIR" &>/dev/null; then
    echo "[1/6] SSH keypair '$KEYPAIR' already exists in OpenStack"
else
    echo "[1/6] Uploading SSH keypair to OpenStack..."
    openstack keypair create --public-key "${SSH_KEY_PATH}.pub" "$KEYPAIR"
fi

# ---------------------------------------------------------------------------
# Step 2: Ensure security group exists
# ---------------------------------------------------------------------------
if openstack security group show "$SECGROUP" &>/dev/null; then
    echo "[2/6] Security group '$SECGROUP' already exists"
else
    echo "[2/6] Creating security group '$SECGROUP'..."
    openstack security group create "$SECGROUP" --description "Slidev MCP Server - SSH, HTTP, HTTPS"
    openstack security group rule create "$SECGROUP" --protocol tcp --dst-port 22 --remote-ip 0.0.0.0/0 --description "SSH"
    openstack security group rule create "$SECGROUP" --protocol tcp --dst-port 80 --remote-ip 0.0.0.0/0 --description "HTTP (ACME)"
    openstack security group rule create "$SECGROUP" --protocol tcp --dst-port 443 --remote-ip 0.0.0.0/0 --description "HTTPS"
fi

# ---------------------------------------------------------------------------
# Step 3: Create the server
# ---------------------------------------------------------------------------
echo "[3/6] Creating server '$SERVER_NAME'..."
openstack server create \
    --flavor "$FLAVOR" \
    --image "$IMAGE" \
    --network "$NETWORK" \
    --security-group "$SECGROUP" \
    --key-name "$KEYPAIR" \
    --wait \
    "$SERVER_NAME" -f table -c id -c name -c status -c addresses

# ---------------------------------------------------------------------------
# Step 4: Get public IP
# ---------------------------------------------------------------------------
echo "[4/6] Retrieving public IP..."
SERVER_IP=$(openstack server show "$SERVER_NAME" -f value -c addresses | grep -oP '\d+\.\d+\.\d+\.\d+' | head -1)

if [ -z "$SERVER_IP" ]; then
    echo "[ERROR] Could not determine server IP. Check: openstack server show $SERVER_NAME"
    exit 1
fi

echo "  Public IP: $SERVER_IP"
echo ""
echo "  >>> Point DNS: $DOMAIN -> $SERVER_IP (A record) <<<"
echo ""

# ---------------------------------------------------------------------------
# Step 5: Wait for SSH
# ---------------------------------------------------------------------------
echo "[5/6] Waiting for SSH to become available..."
for i in $(seq 1 30); do
    if ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -i "$SSH_KEY_PATH" "$SSH_USER@$SERVER_IP" "echo ok" &>/dev/null; then
        echo "  SSH ready after ~${i}0 seconds"
        break
    fi
    if [ "$i" -eq 30 ]; then
        echo "[ERROR] SSH not available after 5 minutes. Server may still be booting."
        echo "  Try manually: ssh -i $SSH_KEY_PATH $SSH_USER@$SERVER_IP"
        exit 1
    fi
    sleep 10
done

# ---------------------------------------------------------------------------
# Step 6: Bootstrap the server via SSH
# ---------------------------------------------------------------------------
echo "[6/6] Bootstrapping server..."
ssh -o StrictHostKeyChecking=no -i "$SSH_KEY_PATH" "$SSH_USER@$SERVER_IP" bash -s -- "$DOMAIN" "$GHCR_REPO" <<'BOOTSTRAP'
set -euo pipefail
DOMAIN="$1"
GHCR_REPO="$2"

echo "--- Installing Docker ---"
sudo apt-get update -qq
sudo apt-get install -y -qq ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -qq
sudo apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo usermod -aG docker "$USER"

echo "--- Creating /opt/slidev-mcp ---"
sudo mkdir -p /opt/slidev-mcp/docker
sudo mkdir -p /opt/slidev-mcp/scripts
sudo chown -R "$USER:$USER" /opt/slidev-mcp

echo "--- Setting up unattended upgrades ---"
sudo apt-get install -y -qq unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades 2>/dev/null || true

echo "--- Setting up backup cron ---"
# Daily backup at 3 AM (script will be deployed with docker-compose)
(crontab -l 2>/dev/null || true; echo "0 3 * * * cd /opt/slidev-mcp && /opt/slidev-mcp/scripts/backup.sh >> /var/log/slidev-mcp-backup.log 2>&1") | sort -u | crontab -

echo "--- Server bootstrap complete ---"
echo "  Docker: $(docker --version)"
echo "  Compose: $(docker compose version)"
echo "  Ready for deployment at /opt/slidev-mcp"
BOOTSTRAP

echo ""
echo "============================================"
echo "  Provisioning complete!"
echo "============================================"
echo ""
echo "  Server:    $SERVER_NAME"
echo "  IP:        $SERVER_IP"
echo "  SSH:       ssh -i $SSH_KEY_PATH $SSH_USER@$SERVER_IP"
echo "  Domain:    $DOMAIN -> $SERVER_IP"
echo ""
echo "  Next steps:"
echo "    1. Point DNS: $DOMAIN -> $SERVER_IP (A record)"
echo "    2. Add GitHub secrets:"
echo "       DEPLOY_HOST=$SERVER_IP"
echo "       DEPLOY_USER=$SSH_USER"
echo "       DEPLOY_SSH_KEY=\$(cat $SSH_KEY_PATH)"
echo "       POSTGRES_PASSWORD=<generate a strong password>"
echo "       ACME_EMAIL=<your email>"
echo "       BACKUP_ENCRYPTION_KEY=<generate a strong passphrase>"
echo "    3. Add GitHub variables:"
echo "       DOMAIN=$DOMAIN"
echo "       DEPLOY_DIR=/opt/slidev-mcp"
echo "    4. Push to main or trigger deploy workflow"
echo ""
