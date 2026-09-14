# Friends of Telford Town Park (FOTTP) — public website

Hugo static site for the registered charity "Friends of Telford Town Park (FOTTP)".
Live at https://www.fottp.org.uk, built and deployed by GitHub Actions to GitHub Pages.
Maintainer: gruntfutuk (GitHub username; not a trustee). Read `docs/HANDOFF.md` for full project state before starting work.

## Environment
- Developed on native Windows (PowerShell). Use PowerShell-compatible commands; other charity members will use GitHub Desktop + VS Code, so keep the toolchain simple.
- Hugo **0.166.0 extended** (winget `Hugo.Hugo.Extended`). The version is pinned in `.github/workflows/hugo.yml`; bump local and CI together.
- Python 3.14+ for any helper scripts: use `int | float` unions and `collections.abc`, not `typing` imports.
- British English spelling throughout content and copy.

## Layout
- `hugo.toml` — site config. `baseURL` is `https://www.fottp.org.uk/`.
- `content/` — Markdown pages. `static/` copied verbatim into `public/`.
- `themes/ananke` — git **submodule** (placeholder theme; a proper theme is still to be chosen). Run `git submodule update --init` after a fresh clone.
- `.github/workflows/hugo.yml` — build (`hugo --minify`) and deploy to Pages on push to `main`.
- `import/` (not yet committed) — raw content scraped from the old site for migration.

## Invariants — do not break
- `static/CNAME` must contain exactly `www.fottp.org.uk`. Removing it drops the custom domain on the next deploy.
- Never commit `public/`, `resources/_gen/` or `.hugo_build.lock` (see `.gitignore`).
- DNS and email for fottp.org / fottp.org.uk are hosted at Fastmail and managed by gruntfutuk — do not suggest moving DNS to Cloudflare.
- The old site (https://www.fottp.co.uk, IONOS MyWebsite Now) is not ours to change; treat it as read-only source material.

## Conventions
- Small, focused commits with plain-English messages.
- Prefer editing `hugo.toml` and Markdown over custom layouts until a theme is chosen.
- Ask before adding third-party services (form backends, analytics); the charity wants minimal tracking and no cookie banner if avoidable.
