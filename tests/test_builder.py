import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from slidev_mcp.builder import MAX_MARKDOWN_SIZE, BuildOrchestrator, BuildResult
from slidev_mcp.config import Settings
from slidev_mcp.errors import BuildFailed, BuildTimeout, MarkdownTooLarge, ThemeNotAllowed


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        build_inbox_dir=str(tmp_path / "builds"),
        slides_dir=str(tmp_path / "slides"),
        builder_container_name="builder",
        build_timeout=10,
    )


@pytest.fixture
def semaphore() -> asyncio.Semaphore:
    return asyncio.Semaphore(3)


@pytest.fixture
def orchestrator(settings: Settings, semaphore: asyncio.Semaphore) -> BuildOrchestrator:
    return BuildOrchestrator(settings, semaphore)


def _mock_process(returncode: int = 0, stdout: bytes = b"", stderr: bytes = b"") -> MagicMock:
    proc = MagicMock()
    proc.returncode = returncode
    proc.communicate = AsyncMock(return_value=(stdout, stderr))
    proc.kill = MagicMock()
    proc.wait = AsyncMock()
    return proc


class TestThemeValidation:
    def test_valid_theme(self, orchestrator: BuildOrchestrator) -> None:
        orchestrator._validate_theme("default")
        orchestrator._validate_theme("seriph")
        orchestrator._validate_theme("apple-basic")

    def test_invalid_theme_not_in_allowlist(self, orchestrator: BuildOrchestrator) -> None:
        with pytest.raises(ThemeNotAllowed):
            orchestrator._validate_theme("not-a-real-theme")

    def test_invalid_theme_bad_format(self, orchestrator: BuildOrchestrator) -> None:
        with pytest.raises(ThemeNotAllowed):
            orchestrator._validate_theme("UPPERCASE")
        with pytest.raises(ThemeNotAllowed):
            orchestrator._validate_theme("has spaces")
        with pytest.raises(ThemeNotAllowed):
            orchestrator._validate_theme("../path-traversal")
        with pytest.raises(ThemeNotAllowed):
            orchestrator._validate_theme("semi;colon")

    def test_empty_theme(self, orchestrator: BuildOrchestrator) -> None:
        with pytest.raises(ThemeNotAllowed):
            orchestrator._validate_theme("")


class TestMarkdownValidation:
    def test_valid_markdown(self, orchestrator: BuildOrchestrator) -> None:
        orchestrator._validate_markdown("# Hello\n\nSome content")

    def test_markdown_too_large(self, orchestrator: BuildOrchestrator) -> None:
        large_markdown = "x" * (MAX_MARKDOWN_SIZE + 1)
        with pytest.raises(MarkdownTooLarge):
            orchestrator._validate_markdown(large_markdown)

    def test_markdown_at_limit(self, orchestrator: BuildOrchestrator) -> None:
        # Exactly at limit should be fine
        orchestrator._validate_markdown("x" * MAX_MARKDOWN_SIZE)


class TestBuild:
    async def test_successful_build(
        self, orchestrator: BuildOrchestrator, settings: Settings
    ) -> None:
        proc = _mock_process(returncode=0)

        async def fake_exec(*args, **kwargs):
            # Simulate the builder creating a dist directory
            build_dir = Path(settings.build_inbox_dir) / "test-uuid"
            dist_dir = build_dir / "dist"
            dist_dir.mkdir(parents=True, exist_ok=True)
            (dist_dir / "index.html").write_text("<html>slides</html>")
            return proc

        with patch("asyncio.create_subprocess_exec", side_effect=fake_exec):
            result = await orchestrator.build("# Slide 1", "default", "test-uuid")

        assert isinstance(result, BuildResult)
        assert result.uuid == "test-uuid"
        assert "/slides/test-uuid/" in result.url
        assert result.build_time_seconds >= 0

        # Verify dist was moved to slides dir
        slides_dir = Path(settings.slides_dir) / "test-uuid"
        assert slides_dir.exists()
        assert (slides_dir / "index.html").exists()

        # Verify build inbox was cleaned up
        build_dir = Path(settings.build_inbox_dir) / "test-uuid"
        assert not build_dir.exists()

    async def test_manifest_written_correctly(
        self, orchestrator: BuildOrchestrator, settings: Settings
    ) -> None:
        proc = _mock_process(returncode=0)
        written_manifest = {}

        async def fake_exec(*args, **kwargs):
            build_dir = Path(settings.build_inbox_dir) / "test-uuid"
            manifest_path = build_dir / "build-manifest.json"
            nonlocal written_manifest
            written_manifest = json.loads(manifest_path.read_text())

            dist_dir = build_dir / "dist"
            dist_dir.mkdir(parents=True, exist_ok=True)
            (dist_dir / "index.html").write_text("<html></html>")
            return proc

        with patch("asyncio.create_subprocess_exec", side_effect=fake_exec):
            await orchestrator.build("# Slides", "seriph", "test-uuid")

        assert written_manifest["theme"] == "seriph"
        assert written_manifest["uuid"] == "test-uuid"
        assert written_manifest["base_path"] == "/slides/test-uuid/"

    async def test_slides_md_written(
        self, orchestrator: BuildOrchestrator, settings: Settings
    ) -> None:
        proc = _mock_process(returncode=0)
        written_slides = ""

        async def fake_exec(*args, **kwargs):
            build_dir = Path(settings.build_inbox_dir) / "test-uuid"
            nonlocal written_slides
            written_slides = (build_dir / "slides.md").read_text()

            dist_dir = build_dir / "dist"
            dist_dir.mkdir(parents=True, exist_ok=True)
            (dist_dir / "index.html").write_text("<html></html>")
            return proc

        with patch("asyncio.create_subprocess_exec", side_effect=fake_exec):
            await orchestrator.build("# My Slides\n\nContent here", "default", "test-uuid")

        assert "# My Slides" in written_slides

    async def test_build_failed(self, orchestrator: BuildOrchestrator, settings: Settings) -> None:
        proc = _mock_process(returncode=1, stderr=b"some error output")

        async def fake_exec(*args, **kwargs):
            # Create the build dir so cleanup works
            build_dir = Path(settings.build_inbox_dir) / "fail-uuid"
            build_dir.mkdir(parents=True, exist_ok=True)
            return proc

        with (
            patch("asyncio.create_subprocess_exec", side_effect=fake_exec),
            pytest.raises(BuildFailed, match="some error output"),
        ):
            await orchestrator.build("# Slides", "default", "fail-uuid")

        # Build inbox should still be cleaned up
        assert not (Path(settings.build_inbox_dir) / "fail-uuid").exists()

    async def test_build_failed_with_error_json(
        self, orchestrator: BuildOrchestrator, settings: Settings
    ) -> None:
        proc = _mock_process(returncode=1)

        async def fake_exec(*args, **kwargs):
            build_dir = Path(settings.build_inbox_dir) / "fail-uuid"
            build_dir.mkdir(parents=True, exist_ok=True)
            error_info = {"exit_code": 1, "stderr": "Detailed error from builder"}
            (build_dir / "error.json").write_text(json.dumps(error_info))
            return proc

        with (
            patch("asyncio.create_subprocess_exec", side_effect=fake_exec),
            pytest.raises(BuildFailed, match="Detailed error from builder"),
        ):
            await orchestrator.build("# Slides", "default", "fail-uuid")

    async def test_build_timeout(self, orchestrator: BuildOrchestrator, settings: Settings) -> None:
        proc = _mock_process()

        async def slow_communicate():
            await asyncio.sleep(100)
            return (b"", b"")

        proc.communicate = slow_communicate

        async def fake_exec(*args, **kwargs):
            build_dir = Path(settings.build_inbox_dir) / "timeout-uuid"
            build_dir.mkdir(parents=True, exist_ok=True)
            return proc

        with (
            patch("asyncio.create_subprocess_exec", side_effect=fake_exec),
            pytest.raises(BuildTimeout),
        ):
            await orchestrator.build("# Slides", "default", "timeout-uuid")

    async def test_overwrite_existing_slides(
        self, orchestrator: BuildOrchestrator, settings: Settings
    ) -> None:
        # Pre-create an existing slides directory
        existing_dir = Path(settings.slides_dir) / "overwrite-uuid"
        existing_dir.mkdir(parents=True)
        (existing_dir / "old.html").write_text("<html>old</html>")

        proc = _mock_process(returncode=0)

        async def fake_exec(*args, **kwargs):
            build_dir = Path(settings.build_inbox_dir) / "overwrite-uuid"
            dist_dir = build_dir / "dist"
            dist_dir.mkdir(parents=True, exist_ok=True)
            (dist_dir / "index.html").write_text("<html>new</html>")
            return proc

        with patch("asyncio.create_subprocess_exec", side_effect=fake_exec):
            await orchestrator.build("# Updated", "default", "overwrite-uuid")

        slides_dir = Path(settings.slides_dir) / "overwrite-uuid"
        assert (slides_dir / "index.html").read_text() == "<html>new</html>"
        assert not (slides_dir / "old.html").exists()

    async def test_missing_dist_raises_build_failed(
        self, orchestrator: BuildOrchestrator, settings: Settings
    ) -> None:
        proc = _mock_process(returncode=0)

        async def fake_exec(*args, **kwargs):
            # Don't create dist dir — simulates builder not producing output
            build_dir = Path(settings.build_inbox_dir) / "no-dist-uuid"
            build_dir.mkdir(parents=True, exist_ok=True)
            return proc

        with (
            patch("asyncio.create_subprocess_exec", side_effect=fake_exec),
            pytest.raises(BuildFailed, match="dist/ directory not found"),
        ):
            await orchestrator.build("# Slides", "default", "no-dist-uuid")
