from slidev_mcp.config import ALLOWED_THEMES, Settings


class TestSettings:
    def test_defaults(self, monkeypatch):
        monkeypatch.delenv("DOMAIN", raising=False)
        monkeypatch.delenv("SLIDES_DOMAIN", raising=False)
        settings = Settings(_env_file=None)
        assert settings.domain == "localhost"
        assert settings.server_transport == "stdio"
        assert settings.server_port == 8000
        assert settings.build_timeout == 120
        assert settings.max_concurrent_builds == 3
        assert settings.slide_ttl_days == 30
        assert settings.gc_interval_hours == 6
        assert settings.log_level == "INFO"
        assert settings.log_format == "json"

    def test_env_override(self, monkeypatch):
        monkeypatch.setenv("DOMAIN", "slides.example.com")
        monkeypatch.setenv("BUILD_TIMEOUT", "60")
        monkeypatch.setenv("SERVER_TRANSPORT", "streamable-http")
        settings = Settings()
        assert settings.domain == "slides.example.com"
        assert settings.build_timeout == 60
        assert settings.server_transport == "streamable-http"

    def test_allowed_themes_populated(self):
        assert len(ALLOWED_THEMES) > 0
        assert "default" in ALLOWED_THEMES
        assert "seriph" in ALLOWED_THEMES

    def test_allowed_themes_are_lowercase_alphanumeric(self):
        import re

        pattern = re.compile(r"^[a-z0-9-]+$")
        for theme in ALLOWED_THEMES:
            assert pattern.match(theme), f"Theme '{theme}' doesn't match allowed format"
