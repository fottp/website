#!/usr/bin/env python3
"""Copy a release of the theme into themes/hextra/ (replacing what is there).

The theme is *copied into this repo*, not attached as a git submodule, so that:
  * Windows checkouts can't rewrite its line endings and break its templates
    (see .gitattributes: themes/hextra/** is forced to LF);
  * the exact code the site is built from is in this repo and reviewable.

Only what a site needs is copied: assets/, data/, i18n/, layouts/, the licence,
theme.toml and the theme's own hugo.toml. Its docs, examples, tests and static/
(Hextra's own branding: favicons, logos) are left out; the site provides its own.

    python scripts/vendor_theme.py            # the release in .github/theme-pin.json
    python scripts/vendor_theme.py v0.12.4    # a specific release

Then re-apply our edits to any overridden file the release changed (the release
watcher's report lists them), build, check the pages, and update the pin.
Standard library only. Set GITHUB_TOKEN to raise GitHub's API rate limit.
"""
from __future__ import annotations

import io
import json
import os
import shutil
import sys
import tarfile
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIN = ROOT / ".github" / "theme-pin.json"
DEST = ROOT / "themes" / "hextra"
KEEP = ("assets/", "data/", "i18n/", "layouts/")
KEEP_FILES = ("LICENSE", "theme.toml", "hugo.toml")


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "vendor-theme", "Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def main() -> int:
    pin = json.loads(PIN.read_text(encoding="utf-8"))
    repo = pin["repo"]
    tag = sys.argv[1] if len(sys.argv) > 1 else pin["tag"]

    ref = json.loads(fetch(f"https://api.github.com/repos/{repo}/git/ref/tags/{tag}"))["object"]
    sha = ref["sha"]
    if ref["type"] == "tag":  # annotated tag: follow it to the commit
        sha = json.loads(fetch(f"https://api.github.com/repos/{repo}/git/tags/{sha}"))["object"]["sha"]

    data = fetch(f"https://api.github.com/repos/{repo}/tarball/{tag}")
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)

    copied = 0
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        for m in tar.getmembers():
            if not m.isfile():
                continue
            rel = m.name.split("/", 1)[1]  # drop the "<owner>-<repo>-<sha>/" prefix
            if not (rel.startswith(KEEP) or rel in KEEP_FILES):
                continue
            out = DEST / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(tar.extractfile(m).read())
            copied += 1

    (DEST / "VENDORED.md").write_text(
        f"""# This is a copy of {repo} {tag}

Source: https://github.com/{repo}/releases/tag/{tag} (commit {sha})
Copied: {date.today().isoformat()} by `scripts/vendor_theme.py`
Licence: MIT — see `LICENSE` in this folder.

Included: `assets/`, `data/`, `i18n/`, `layouts/`, `LICENSE`, `theme.toml`, `hugo.toml`.
Left out: the theme's docs, examples, tests, and `static/` (its own favicons and logos; this site has its own).

**Do not edit anything in this folder.** The next update replaces it wholesale. Site-specific changes
live in the site's own `layouts/`, `assets/`, `data/` and `static/`, which override the theme's;
`.github/theme-pin.json` lists which theme files those overrides replace or depend on.
To update: see `docs/HANDOFF.md`, "Theme upkeep".
""",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Copied {copied} files from {repo} {tag} ({sha[:9]}) into {DEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
