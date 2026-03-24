import asyncio
import json
import logging
import re
import shutil
import time
from dataclasses import dataclass
from pathlib import Path

from slidev_mcp.config import ALLOWED_THEMES, Settings
from slidev_mcp.errors import BuildFailed, BuildTimeout, MarkdownTooLarge, ThemeNotAllowed

logger = logging.getLogger(__name__)

THEME_NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
MAX_MARKDOWN_SIZE = 1_000_000  # 1 MB


@dataclass
class BuildResult:
    uuid: str
    url: str
    build_time_seconds: float


class BuildOrchestrator:
    def __init__(self, settings: Settings, semaphore: asyncio.Semaphore) -> None:
        self._settings = settings
        self._semaphore = semaphore

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

        build_dir = Path(self._settings.build_inbox_dir) / uuid
        slides_dir = Path(self._settings.slides_dir) / uuid

        try:
            # Write build inputs
            build_dir.mkdir(parents=True, exist_ok=True)

            manifest = {
                "theme": theme,
                "uuid": uuid,
                "base_path": f"/slides/{uuid}/",
            }
            (build_dir / "build-manifest.json").write_text(json.dumps(manifest))
            (build_dir / "slides.md").write_text(markdown, encoding="utf-8")

            # Run build in builder container
            start = time.monotonic()
            proc = await asyncio.create_subprocess_exec(
                "docker",
                "exec",
                self._settings.builder_container_name,
                "bun",
                "run",
                "/app/build-job.ts",
                f"/data/builds/{uuid}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                _stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=self._settings.build_timeout,
                )
            except TimeoutError:
                proc.kill()
                await proc.wait()
                raise BuildTimeout(self._settings.build_timeout) from None

            elapsed = time.monotonic() - start

            if proc.returncode != 0:
                # Try to read error.json for structured error info
                error_file = build_dir / "error.json"
                if error_file.exists():
                    error_info = json.loads(error_file.read_text())
                    raise BuildFailed(error_info.get("stderr", "Unknown error"))
                raise BuildFailed(stderr.decode("utf-8", errors="replace"))

            # Move dist to slides directory
            dist_dir = build_dir / "dist"
            if not dist_dir.exists():
                raise BuildFailed("Build completed but dist/ directory not found")

            if slides_dir.exists():
                shutil.rmtree(slides_dir)
            shutil.move(str(dist_dir), str(slides_dir))

            slides_host = self._settings.slides_domain or self._settings.domain
            url = f"https://{slides_host}/slides/{uuid}/"
            logger.info(
                "Build completed",
                extra={"uuid": uuid, "theme": theme, "duration": round(elapsed, 2)},
            )
            return BuildResult(uuid=uuid, url=url, build_time_seconds=round(elapsed, 2))

        finally:
            # Clean up build inbox
            if build_dir.exists():
                shutil.rmtree(build_dir)
