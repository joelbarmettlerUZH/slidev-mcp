class SlidevMcpError(Exception):
    """Base error for all Slidev MCP errors."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


class ThemeNotAllowed(SlidevMcpError):
    def __init__(self, theme: str) -> None:
        super().__init__("theme_not_allowed", f"Theme '{theme}' is not in the allowlist")


class UuidSealed(SlidevMcpError):
    def __init__(self, uuid: str) -> None:
        super().__init__("uuid_sealed", f"UUID '{uuid}' is sealed and cannot be modified")


class UuidForeign(SlidevMcpError):
    def __init__(self, uuid: str) -> None:
        super().__init__("uuid_foreign", f"UUID '{uuid}' belongs to a different session")


class BuildFailed(SlidevMcpError):
    def __init__(self, stderr: str) -> None:
        super().__init__("build_failed", f"Slidev build failed: {stderr[:500]}")


class BuildTimeout(SlidevMcpError):
    def __init__(self, timeout: int) -> None:
        super().__init__("build_timeout", f"Build exceeded timeout of {timeout}s")


class MarkdownTooLarge(SlidevMcpError):
    def __init__(self, size: int, limit: int) -> None:
        super().__init__(
            "markdown_too_large",
            f"Markdown size ({size} bytes) exceeds limit ({limit} bytes)",
        )


class InvalidUuid(SlidevMcpError):
    def __init__(self, uuid: str) -> None:
        super().__init__("invalid_uuid", f"UUID '{uuid}' is not a valid UUID v4 format")


class ConcurrentLimitReached(SlidevMcpError):
    def __init__(self) -> None:
        super().__init__("concurrent_limit", "Build concurrency limit reached; retry later")
