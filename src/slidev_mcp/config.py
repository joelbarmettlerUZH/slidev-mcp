from pydantic_settings import BaseSettings

ALLOWED_THEMES: list[str] = [
    # Official @slidev/theme-* packages
    "default",
    "seriph",
    "apple-basic",
    "bricks",
    "shibainu",
    # Community slidev-theme-* packages (sorted by npm downloads)
    "ehl2022",
    "cobalt",
    "academic",
    "scholarly",
    "neversink",
    "meetup",
    "penguin",
    "geist",
    "purplin",
    "nmt",
    "nearform",
    "mistica",
    "alchemmist",
    "the-unnamed",
    "whulug",
    "one-purple-unicorn-pro",
    "nord",
    "light-icons",
    "vibe",
    "greycat",
    "neocarbon",
    "umn",
    "field-manual",
    "scorpion",
    "ucsf",
    "dataerai",
    "measurelab",
    "academic-schober",
    "swiss-ai-hub",
]


class Settings(BaseSettings):
    model_config = {"env_prefix": "", "env_file": ".env", "extra": "ignore"}

    domain: str = "localhost"
    slides_domain: str = ""
    database_url: str = "postgresql+asyncpg://slidev:slidev@localhost:5432/slidev"
    slides_dir: str = "/data/slides"
    build_inbox_dir: str = "/data/builds"
    builder_container_name: str = "builder"
    build_timeout: int = 120
    max_concurrent_builds: int = 3
    slide_ttl_days: int = 30
    gc_interval_hours: int = 6
    server_transport: str = "stdio"
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    log_level: str = "INFO"
    log_format: str = "json"
