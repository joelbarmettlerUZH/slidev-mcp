import logging
import re

import httpx

from slidev_mcp.config import ALLOWED_THEMES, Settings
from slidev_mcp.errors import BuildFailed, BuildTimeout, MarkdownTooLarge, ThemeNotAllowed

logger = logging.getLogger(__name__)

THEME_NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
MAX_MARKDOWN_SIZE = 1_000_000  # 1 MB


class BuildResult:
    def __init__(self, uuid: str, url: str, build_time_seconds: float, html: str = "") -> None:
        self.uuid = uuid
        self.url = url
        self.build_time_seconds = build_time_seconds
        self.html = html


class BuildOrchestrator:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = httpx.AsyncClient(
            base_url=f"http://{settings.builder_host}:{settings.builder_port}",
            timeout=httpx.Timeout(settings.build_timeout + 5, connect=10),
        )

    def _validate_theme(self, theme: str) -> None:
        if not THEME_NAME_PATTERN.match(theme):
            raise ThemeNotAllowed(theme)
        if theme not in ALLOWED_THEMES:
            raise ThemeNotAllowed(theme)

    def _validate_markdown(self, markdown: str) -> None:
        size = len(markdown.encode("utf-8"))
        if size > MAX_MARKDOWN_SIZE:
            raise MarkdownTooLarge(size, MAX_MARKDOWN_SIZE)

    async def build(self, markdown: str, theme: str, uuid: str) -> BuildResult:
        self._validate_theme(theme)
        self._validate_markdown(markdown)

        try:
            resp = await self._client.post(
                "/build",
                json={
                    "markdown": markdown,
                    "theme": theme,
                    "uuid": uuid,
                    "base_path": f"/slides/{uuid}/",
                },
            )
        except httpx.TimeoutException:
            raise BuildTimeout(self._settings.build_timeout) from None

        if resp.status_code != 200:
            data = resp.json()
            error_code = data.get("error", "build_failed")
            details = data.get("details", "Unknown error")
            raise BuildFailed(f"[{error_code}] {details}")

        data = resp.json()
        slides_host = self._settings.slides_domain or self._settings.domain
        url = f"https://{slides_host}/slides/{uuid}/"

        elapsed = data.get("build_time_seconds", 0)
        logger.info(
            "Build completed",
            extra={"uuid": uuid, "theme": theme, "duration": elapsed},
        )
        html = data.get("html", "")
        return BuildResult(uuid=uuid, url=url, build_time_seconds=elapsed, html=html)

    async def close(self) -> None:
        await self._client.aclose()
