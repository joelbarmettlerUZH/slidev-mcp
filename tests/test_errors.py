from slidev_mcp.errors import (
    BuildFailed,
    BuildTimeout,
    ConcurrentLimitReached,
    MarkdownTooLarge,
    SlidevMcpError,
    ThemeNotAllowed,
    UuidForeign,
    UuidSealed,
)


class TestErrors:
    def test_all_inherit_from_base(self):
        errors = [
            ThemeNotAllowed("bad-theme"),
            UuidSealed("some-uuid"),
            UuidForeign("some-uuid"),
            BuildFailed("stderr output"),
            BuildTimeout(120),
            MarkdownTooLarge(2_000_000, 1_000_000),
            ConcurrentLimitReached(),
        ]
        for error in errors:
            assert isinstance(error, SlidevMcpError)

    def test_error_codes(self):
        assert ThemeNotAllowed("x").code == "theme_not_allowed"
        assert UuidSealed("x").code == "uuid_sealed"
        assert UuidForeign("x").code == "uuid_foreign"
        assert BuildFailed("x").code == "build_failed"
        assert BuildTimeout(60).code == "build_timeout"
        assert MarkdownTooLarge(2, 1).code == "markdown_too_large"
        assert ConcurrentLimitReached().code == "concurrent_limit"

    def test_build_failed_truncates_stderr(self):
        long_stderr = "x" * 1000
        error = BuildFailed(long_stderr)
        assert len(error.message) < 600
