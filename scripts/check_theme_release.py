#!/usr/bin/env python3
"""Has the theme published a release newer than the one this site is pinned to?

Reads .github/theme-pin.json, asks GitHub for the theme's latest (non-draft,
non-prerelease) release, and if it is newer writes a Markdown report saying:

  * what the release is, with a link to its notes;
  * which of the files we have OVERRIDDEN (copied and edited) the theme changed
    between the pinned release and the new one -- those need re-merging by hand;
  * which files our code DEPENDS ON (partials, CSS) changed -- worth a look.

It never changes anything. Standard library only, so it runs anywhere.

    python scripts/check_theme_release.py                    # print the result
    python scripts/check_theme_release.py --report out.md    # also write the report
    python scripts/check_theme_release.py --github-output    # for GitHub Actions

Set GITHUB_TOKEN to raise GitHub's API rate limit (the Actions workflow does).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

PIN = Path(__file__).resolve().parent.parent / ".github" / "theme-pin.json"


def api(path: str):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "theme-release-watch")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def version(tag: str) -> tuple[int, ...]:
    return tuple(int(n) for n in re.findall(r"\d+", tag)[:3])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", help="write the Markdown report to this file")
    ap.add_argument("--github-output", action="store_true", help="write outputs for GitHub Actions")
    args = ap.parse_args()

    pin = json.loads(PIN.read_text(encoding="utf-8"))
    repo, pinned = pin["repo"], pin["tag"]

    try:
        latest = api(f"/repos/{repo}/releases/latest")
    except urllib.error.URLError as e:
        print(f"Could not reach GitHub: {e}", file=sys.stderr)
        return 2
    new_tag = latest["tag_name"]
    newer = version(new_tag) > version(pinned)

    outputs = {"newer": str(newer).lower(), "latest": new_tag, "pinned": pinned}
    if args.github_output and os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
            f.writelines(f"{k}={v}\n" for k, v in outputs.items())

    if not newer:
        print(f"Up to date: pinned to {repo} {pinned}; latest release is {new_tag}.")
        return 0

    files = api(f"/repos/{repo}/compare/{pinned}...{new_tag}").get("files", [])
    changed = {f["filename"]: f for f in files}
    ours = [f for f in pin["overrides"] if f in changed]
    deps = [f for f in pin["depends_on"] if f in changed]

    def line(name: str) -> str:
        f = changed[name]
        return f"- `{name}` (+{f['additions']} / -{f['deletions']})"

    body = (latest.get("body") or "").strip()
    if len(body) > 1500:
        body = body[:1500].rstrip() + "\n\n…(notes shortened; see the release page)"
    report = [
        f"# {repo} {new_tag} is available (pinned to {pinned})",
        "",
        f"Release notes: {latest['html_url']}",
        f"All changes: https://github.com/{repo}/compare/{pinned}...{new_tag}",
        "",
        "## Files we have copied or edited that changed upstream (re-merge by hand)",
        *([line(n) for n in ours] or ["- none — our overrides are unaffected"]),
        "",
        "## Files our code relies on that changed (worth a look)",
        *([line(n) for n in deps] or ["- none"]),
        "",
        f"{len(files)} files changed in total between {pinned} and {new_tag}.",
        "",
        "## Release notes",
        "",
        body or "(none published)",
        "",
        "## To update",
        "1. Read the two lists above; view the exact changes on the compare page.",
        f"2. Run `python scripts/vendor_theme.py {new_tag}` (replaces themes/hextra/), then re-apply our edits to any changed file listed above.",
        "3. Build (`hugo --minify --logLevel warn`), check the pages by eye (open the mobile menu too), then set `tag` in `.github/theme-pin.json` to the new release.",
    ]
    text = "\n".join(report) + "\n"
    print(text)
    if args.report:
        Path(args.report).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
