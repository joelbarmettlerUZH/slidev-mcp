import httpx
import pytest

from slidev_mcp.builder import MAX_MARKDOWN_SIZE, BuildOrchestrator, BuildResult
from slidev_mcp.config import Settings
from slidev_mcp.errors import BuildFailed, BuildTimeout, MarkdownTooLarge, ThemeNotAllowed


@pytest.fixture
def settings() -> Settings:
    return Settings(
        builder_host="localhost",
        builder_port=9999,
        build_timeout=10,
    )


@pytest.fixture
def orchestrator(settings: Settings) -> BuildOrchestrator:
    return BuildOrchestrator(settings)


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
        orchestrator._validate_markdown("x" * MAX_MARKDOWN_SIZE)


class TestBuild:
    async def test_successful_build(self, orchestrator: BuildOrchestrator) -> None:
        transport = httpx.MockTransport(
            lambda req: httpx.Response(200, json={"uuid": "test-uuid", "build_time_seconds": 3.5})
        )
        orchestrator._client = httpx.AsyncClient(transport=transport, base_url="http://test")

        result = await orchestrator.build("# Slide 1", "default", "test-uuid")

        assert isinstance(result, BuildResult)
        assert result.uuid == "test-uuid"
        assert "/slides/test-uuid/" in result.url
        assert result.build_time_seconds == 3.5

    async def test_build_sends_correct_payload(self, orchestrator: BuildOrchestrator) -> None:
        captured = {}

        def handler(req: httpx.Request) -> httpx.Response:
            captured["json"] = req.content
            captured["url"] = str(req.url)
            return httpx.Response(200, json={"uuid": "test-uuid", "build_time_seconds": 1.0})

        orchestrator._client = httpx.AsyncClient(
            transport=httpx.MockTransport(handler), base_url="http://test"
        )

        await orchestrator.build("# My Slides\n\nContent", "seriph", "test-uuid")

        import json

        payload = json.loads(captured["json"])
        assert payload["markdown"] == "# My Slides\n\nContent"
        assert payload["theme"] == "seriph"
        assert payload["uuid"] == "test-uuid"
        assert payload["base_path"] == "/slides/test-uuid/"

    async def test_build_failed(self, orchestrator: BuildOrchestrator) -> None:
        transport = httpx.MockTransport(
            lambda req: httpx.Response(
                500, json={"error": "build_failed", "details": "some error output"}
            )
        )
        orchestrator._client = httpx.AsyncClient(transport=transport, base_url="http://test")

        with pytest.raises(BuildFailed, match="some error output"):
            await orchestrator.build("# Slides", "default", "fail-uuid")

    async def test_build_timeout(self, orchestrator: BuildOrchestrator) -> None:
        def handler(req: httpx.Request) -> httpx.Response:
            raise httpx.ReadTimeout("timed out")

        orchestrator._client = httpx.AsyncClient(
            transport=httpx.MockTransport(handler), base_url="http://test"
        )

        with pytest.raises(BuildTimeout):
            await orchestrator.build("# Slides", "default", "timeout-uuid")

    async def test_theme_not_found_from_builder(self, orchestrator: BuildOrchestrator) -> None:
        transport = httpx.MockTransport(
            lambda req: httpx.Response(
                400, json={"error": "theme_not_found", "details": "Theme directory not found"}
            )
        )
        orchestrator._client = httpx.AsyncClient(transport=transport, base_url="http://test")

        with pytest.raises(BuildFailed, match="theme_not_found"):
            await orchestrator.build("# Slides", "default", "test-uuid")
