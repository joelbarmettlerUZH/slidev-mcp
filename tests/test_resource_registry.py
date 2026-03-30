import logging
from pathlib import Path

import pytest

from slidev_mcp.resource_registry import RESOURCE_MAP, load_resources


@pytest.fixture
def vendor_dir(tmp_path: Path) -> Path:
    """Create a mock vendor directory with upstream docs."""
    d = tmp_path / "vendor"
    for uri, ref in RESOURCE_MAP.items():
        if ref.startswith("vendor:"):
            rel = ref.removeprefix("vendor:")
            path = d / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# Content for {uri}\n\nMock content.")
    return d


@pytest.fixture
def package_dir() -> Path:
    """Return the real package directory with hand-authored resources."""
    return Path(__file__).parent.parent / "src" / "slidev_mcp"


class TestLoadResources:
    def test_loads_all_resources_with_vendor(self, vendor_dir: Path, package_dir: Path) -> None:
        resources = load_resources(vendor_dir, package_dir)
        for uri, _ref in RESOURCE_MAP.items():
            assert uri in resources, f"Missing resource: {uri}"
            assert len(resources[uri]) > 0

    def test_package_resources_have_content(self, vendor_dir: Path, package_dir: Path) -> None:
        resources = load_resources(vendor_dir, package_dir)
        assert "slidev://themes/installed" in resources
        assert "default" in resources["slidev://themes/installed"]
        assert "slidev://examples/minimal" in resources
        assert "# Welcome" in resources["slidev://examples/minimal"]

    def test_missing_vendor_file_logs_warning(
        self, tmp_path: Path, package_dir: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        empty_vendor = tmp_path / "empty_vendor"
        empty_vendor.mkdir()
        with caplog.at_level(logging.WARNING):
            resources = load_resources(empty_vendor, package_dir)

        # Vendor-based resources should be missing
        vendor_uris = [uri for uri, ref in RESOURCE_MAP.items() if ref.startswith("vendor:")]
        for uri in vendor_uris:
            assert uri not in resources

        assert "Resource file missing" in caplog.text

    def test_missing_package_file_logs_warning(
        self, vendor_dir: Path, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        empty_package = tmp_path / "empty_package"
        empty_package.mkdir()
        with caplog.at_level(logging.WARNING):
            resources = load_resources(vendor_dir, empty_package)

        # Package-based resources should be missing
        package_uris = [uri for uri, ref in RESOURCE_MAP.items() if ref.startswith("package:")]
        for uri in package_uris:
            assert uri not in resources

    def test_theme_guide_loaded(self, vendor_dir: Path, package_dir: Path) -> None:
        resources = load_resources(vendor_dir, package_dir)
        assert "slidev://themes/guide" in resources
        assert "Quick Reference" in resources["slidev://themes/guide"]
        assert "neocarbon" in resources["slidev://themes/guide"]

    def test_resource_map_has_expected_uris(self) -> None:
        expected_uris = [
            "slidev://guide/syntax",
            "slidev://guide/animations",
            "slidev://guide/layout",
            "slidev://guide/theme-addon",
            "slidev://builtin/components",
            "slidev://builtin/layouts",
            "slidev://themes/installed",
            "slidev://themes/guide",
            "slidev://examples/minimal",
            "slidev://examples/full_demo",
        ]
        for uri in expected_uris:
            assert uri in RESOURCE_MAP
