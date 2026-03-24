import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Maps resource URIs to paths relative to vendor_dir or package_dir.
# Entries starting with "vendor:" are resolved against vendor_dir.
# Entries starting with "package:" are resolved against package_dir.
RESOURCE_MAP: dict[str, str] = {
    "slidev://guide/syntax": "vendor:guide/syntax.md",
    "slidev://guide/animations": "vendor:guide/animations.md",
    "slidev://guide/layout": "vendor:guide/layout.md",
    "slidev://guide/theme-addon": "vendor:guide/theme-addon.md",
    "slidev://builtin/components": "vendor:builtin/components.md",
    "slidev://builtin/layouts": "vendor:builtin/layouts.md",
    "slidev://themes/installed": "package:resources/installed_themes.md",
    "slidev://examples/minimal": "package:resources/examples/minimal.md",
    "slidev://examples/full_demo": "package:resources/examples/full_demo.md",
}


def _resolve_path(ref: str, vendor_dir: Path, package_dir: Path) -> Path:
    if ref.startswith("vendor:"):
        return vendor_dir / ref.removeprefix("vendor:")
    if ref.startswith("package:"):
        return package_dir / ref.removeprefix("package:")
    msg = f"Unknown path prefix in resource ref: {ref}"
    raise ValueError(msg)


def load_resources(vendor_dir: Path, package_dir: Path) -> dict[str, str]:
    """Load all resources from disk. Returns {uri: content}.

    Logs warnings for missing files but does not crash.
    """
    resources: dict[str, str] = {}

    for uri, ref in RESOURCE_MAP.items():
        path = _resolve_path(ref, vendor_dir, package_dir)
        if not path.exists():
            logger.warning("Resource file missing for %s: %s", uri, path)
            continue
        resources[uri] = path.read_text(encoding="utf-8")

    return resources
