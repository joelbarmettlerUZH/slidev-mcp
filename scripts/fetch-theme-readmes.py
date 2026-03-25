#!/usr/bin/env python3
"""Fetch README and example.md files for all themes and merge them into a single resource.

Run during Docker build or via `make bootstrap` to populate
src/slidev_mcp/resources/themes/ with per-theme documentation.

Usage:
  python3 scripts/fetch-theme-readmes.py [themes.json] [output_dir]
"""

import json
import sys
import urllib.request
from pathlib import Path

_default_themes = Path(__file__).parent.parent / "builder" / "themes.json"
_default_output = Path(__file__).parent.parent / "src" / "slidev_mcp" / "resources" / "themes"

THEMES_JSON = Path(sys.argv[1]) if len(sys.argv) > 1 else _default_themes
OUTPUT_DIR = Path(sys.argv[2]) if len(sys.argv) > 2 else _default_output


def fetch_url(url: str, timeout: int = 15) -> str | None:
    """Fetch text content from a URL. Returns None on failure."""
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json, text/plain, */*"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def fetch_readme_from_npm(package: str) -> str | None:
    """Fetch README from npm registry."""
    url = f"https://registry.npmjs.org/{package}"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            readme = data.get("readme", "")
            return readme if readme and len(readme.strip()) > 50 else None
    except Exception:
        return None


def repo_to_example_url(repo: str) -> str | None:
    """Convert GitHub repo URL to raw URL for example.md."""
    if "github.com" not in repo:
        return None
    parts = repo.replace("https://github.com/", "").split("/tree/")
    if len(parts) == 2:
        user_repo, branch_path = parts
        branch, path = branch_path.split("/", 1)
        return f"https://raw.githubusercontent.com/{user_repo}/{branch}/{path}/example.md"
    return f"https://raw.githubusercontent.com/{parts[0]}/HEAD/example.md"


def main() -> None:
    config = json.loads(THEMES_JSON.read_text())
    themes = config["themes"]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    count = 0
    for name, entry in sorted(themes.items()):
        package = entry["package"]
        repo = entry.get("repo", "")
        parts: list[str] = []

        # 1. Fetch README from npm
        print(f"  [{name}] Fetching README from npm...", end="")
        readme = fetch_readme_from_npm(package)
        if readme:
            parts.append(readme.rstrip())
            print(" OK")
        else:
            print(" not found")

        # 2. Fetch example.md from GitHub
        example_url = repo_to_example_url(repo)
        if example_url:
            print(f"  [{name}] Fetching example.md from GitHub...", end="")
            example = fetch_url(example_url)
            if example and len(example.strip()) > 20:
                parts.append(
                    "\n\n---\n\n"
                    "# Example Slides\n\n"
                    "The following is the theme's example presentation showing available "
                    "layouts, components, and features:\n\n"
                    "````markdown\n" + example.rstrip() + "\n````"
                )
                print(" OK")
            else:
                print(" not found")

        if parts:
            (OUTPUT_DIR / f"{name}.md").write_text("\n".join(parts) + "\n", encoding="utf-8")
            count += 1
        else:
            print(f"  [{name}] SKIP — no content found")

    print(f"\nFetched {count}/{len(themes)} theme resources to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
