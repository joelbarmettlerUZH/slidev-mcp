FROM oven/bun:latest

WORKDIR /app

# Copy package files and config
COPY bunfig.toml ./
COPY package.json ./

# Install dependencies (lifecycle scripts disabled via bunfig.toml)
RUN bun install --frozen-lockfile

# Copy template and build script
COPY template/ ./template/
COPY build-job.ts ./

# Create non-root builder user (GID 1000 may already exist in base image)
RUN getent group 1000 || groupadd -g 1000 builder; \
    id -u 1000 2>/dev/null || useradd -u 1000 -g 1000 -m builder; \
    mkdir -p /data/builds /data/slides && \
    chown -R 1000:1000 /app /data/builds /data/slides

USER 1000

CMD ["sleep", "infinity"]
