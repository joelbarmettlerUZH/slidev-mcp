import logging
import re
from dataclasses import dataclass, field

import httpx

from slidev_mcp.config import ALLOWED_THEMES, Settings
from slidev_mcp.errors import BuildFailed, BuildTimeout, MarkdownTooLarge, ThemeNotAllowed

logger = logging.getLogger(__name__)

THEME_NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
MAX_MARKDOWN_SIZE = 1_000_000  # 1 MB


@dataclass(frozen=True, slots=True)
class BuildResult:
    uuid: str
    url: str
    build_time_seconds: float
    html: str = ""
    preview_base64: str = ""


@dataclass(frozen=True, slots=True)
class ExportResult:
    uuid: str
    export_time_seconds: float
    url: str = ""
    images_base64: list[str] = field(default_factory=list)


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

    async def build(
        self, markdown: str, theme: str, uuid: str, color_schema: str = "light"
    ) -> BuildResult:
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
                    "color_schema": color_schema,
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
        preview_base64 = data.get("preview_base64", "")
        return BuildResult(
            uuid=uuid, url=url, build_time_seconds=elapsed, html=html, preview_base64=preview_base64
        )

    async def export(
        self, markdown: str, theme: str, uuid: str, fmt: str = "pdf", color_schema: str = "light"
    ) -> ExportResult:
        """Export a slide deck as PDF or PNG screenshots."""
        self._validate_theme(theme)

        try:
            resp = await self._client.post(
                "/export",
                json={
                    "markdown": markdown,
                    "theme": theme,
                    "uuid": uuid,
                    "format": fmt,
                    "color_schema": color_schema,
                },
                timeout=httpx.Timeout(180, connect=10),
            )
        except httpx.TimeoutException:
            raise BuildTimeout(180) from None

        if resp.status_code != 200:
            data = resp.json()
            error_code = data.get("error", "export_failed")
            details = data.get("details", "Unknown error")
            raise BuildFailed(f"[{error_code}] {details}")

        data = resp.json()
        elapsed = data.get("export_time_seconds", 0)
        logger.info(
            "Export completed",
            extra={"uuid": uuid, "format": fmt, "duration": elapsed},
        )

        if fmt == "png":
            return ExportResult(
                uuid=uuid,
                export_time_seconds=elapsed,
                images_base64=data.get("images_base64", []),
            )

        slides_host = self._settings.slides_domain or self._settings.domain
        filename = data.get("filename", "slides-export.pdf")
        url = f"https://{slides_host}/slides/{uuid}/{filename}"
        return ExportResult(uuid=uuid, url=url, export_time_seconds=elapsed)

    async def close(self) -> None:
        await self._client.aclose()
