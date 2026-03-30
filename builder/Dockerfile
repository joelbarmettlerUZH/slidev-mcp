FROM oven/bun:latest

# Install Playwright system dependencies as root (Chromium needs system libs)
USER root
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
      fonts-noto-color-emoji \
    && rm -rf /var/lib/apt/lists/*
RUN bunx playwright install chromium --with-deps

# Create non-root user — avoids expensive chown of node_modules later
RUN getent group 1000 || groupadd -g 1000 builder; \
    id -u 1000 2>/dev/null || useradd -u 1000 -g 1000 -m builder; \
    mkdir -p /app /data/builds /data/slides && \
    chown -R 1000:1000 /app /data

WORKDIR /app
USER 1000

# Copy config and scripts (owned by builder user)
COPY --chown=1000:1000 bunfig.toml themes.json ./
COPY --chown=1000:1000 scripts/ ./scripts/

# Generate per-theme project directories
RUN bun run scripts/init-themes.ts

# Pre-warm bun's global cache by installing the first theme (downloads @slidev/cli etc.)
RUN cd themes/default && bun install

# Install remaining themes in parallel — cache is pre-warmed so these are fast
RUN for dir in themes/*/; do \
      [ "$dir" = "themes/default/" ] && continue; \
      (cd /app/$dir && bun install) & \
    done; wait

# Copy build scripts and server
COPY --chown=1000:1000 build-job.ts export-job.ts server.ts ./

# Validate all themes — remove any that fail to build
RUN bun run scripts/validate-themes.ts --remove-broken

EXPOSE 3000
CMD ["bun", "run", "server.ts"]
