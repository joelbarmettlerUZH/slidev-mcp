from pydantic import Field
from pydantic_settings import BaseSettings

ALLOWED_THEMES: list[str] = [
    # Official @slidev/theme-* packages (MIT, maintained by Slidev team)
    "default",
    "seriph",
    "apple-basic",
    "bricks",
    "shibainu",
    # Community slidev-theme-* packages (all MIT or Apache-2.0, build-validated)
    "academic",
    "cobalt",
    "dracula",
    "eloc",
    "field-manual",
    "frankfurt",
    "geist",
    "neocarbon",
    "neversink",
    "nord",
    "penguin",
    "purplin",
    "scholarly",
    "swiss-ai-hub",
    "the-unnamed",
    "unicorn",
    "vibe",
    "vuetiful",
    "zhozhoba",
]


class Settings(BaseSettings):
    model_config = {"env_prefix": "", "env_file": ".env", "extra": "ignore"}

    domain: str = Field(
        default="localhost",
        description="Public domain for the MCP API endpoint",
    )
    slides_domain: str = Field(
        default="",
        description="Separate domain for serving slides (origin isolation). Falls back to domain.",
    )
    database_url: str = Field(
        default="postgresql+asyncpg://slidev:slidev@localhost:5432/slidev",
        description="PostgreSQL async connection string",
    )
    slides_dir: str = Field(
        default="/data/slides",
        description="Directory where built slide decks are stored",
    )
    builder_host: str = Field(
        default="builder",
        description="Hostname of the builder HTTP service",
    )
    builder_port: int = Field(
        default=3000,
        ge=1,
        le=65535,
        description="Port of the builder HTTP service",
    )
    build_timeout: int = Field(
        default=120,
        ge=10,
        le=600,
        description="Maximum seconds allowed for a single slide build",
    )
    max_concurrent_builds: int = Field(
        default=3,
        ge=1,
        le=20,
        description="Maximum number of parallel builds",
    )
    slide_ttl_days: int = Field(
        default=30,
        ge=1,
        description="Days before sealed slides are garbage-collected",
    )
    gc_interval_hours: int = Field(
        default=6,
        ge=1,
        description="Hours between garbage-collection runs",
    )
    server_transport: str = Field(
        default="stdio",
        pattern=r"^(stdio|streamable-http)$",
        description="MCP transport protocol: 'stdio' or 'streamable-http'",
    )
    server_host: str = Field(
        default="0.0.0.0",
        description="Bind address for HTTP transport",
    )
    server_port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="Bind port for HTTP transport",
    )
    log_level: str = Field(
        default="INFO",
        pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Python log level",
    )
    log_format: str = Field(
        default="json",
        pattern=r"^(json|text)$",
        description="Log output format: 'json' or 'text'",
    )
