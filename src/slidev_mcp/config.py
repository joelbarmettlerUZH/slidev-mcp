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

    domain: str = "localhost"
    slides_domain: str = ""
    database_url: str = "postgresql+asyncpg://slidev:slidev@localhost:5432/slidev"
    slides_dir: str = "/data/slides"
    builder_host: str = "builder"
    builder_port: int = 3000
    build_timeout: int = 120
    max_concurrent_builds: int = 3
    slide_ttl_days: int = 30
    gc_interval_hours: int = 6
    server_transport: str = "stdio"
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    log_level: str = "INFO"
    log_format: str = "json"
