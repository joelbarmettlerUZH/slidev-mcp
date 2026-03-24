#!/usr/bin/env bash
set -euo pipefail

# Pin to the Slidev version matching builder/package.json
SLIDEV_REF="v52.14.1"
REPO_URL="https://github.com/slidevjs/slidev.git"
VENDOR_DIR="vendor/slidev-docs"

cd "$(dirname "$0")/.."

if [ -d "$VENDOR_DIR/.git" ]; then
    echo "Updating existing vendor/slidev-docs..."
    cd "$VENDOR_DIR"
    git fetch origin
    git checkout "$SLIDEV_REF" -- docs/
    cd -
else
    echo "Cloning slidev docs (sparse checkout)..."
    mkdir -p "$VENDOR_DIR"
    cd "$VENDOR_DIR"
    git init
    git remote add origin "$REPO_URL"
    git config core.sparseCheckout true
    echo "docs/" > .git/info/sparse-checkout
    git fetch --depth 1 origin "$SLIDEV_REF"
    git checkout FETCH_HEAD
    cd -
fi

echo "Slidev docs vendored at ref: $SLIDEV_REF"
