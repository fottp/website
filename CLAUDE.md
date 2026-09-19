# FOTTP public website
Hugo site for charity FOTTP → https://www.fottp.org.uk (GitHub Pages). Maintainer: gruntfutuk (GitHub username; not a trustee). Read `docs/HANDOFF.md` first.
Proof-of-concept beside https://www.fottp.co.uk (IONOS, run by a current trustee) and old WordPress archive https://friendsoftelfordtownpark.org — both read-only, never change them.

## Environment
- Windows; editors use GitHub Desktop+VS Code or Sveltia CMS (`/admin/`) — keep toolchain simple.
- Hugo **0.166.0 extended**, pinned in `.github/workflows/hugo.yml` — bump local and CI together.
- Python 3.14+ via **uv**, not pip. British English.
- Photos: ≤1600px, JPEG q~82 before committing.

## Layout
- `hugo.toml`: menu, Web3Forms keys, theme params.
- `content/`: Markdown page bundles; images stay beside their page.
- `layouts/`, `assets/css/custom.css`, `data/`: our theme overrides (HANDOFF.md "Theme"). Self-hosted only, no CDNs. `static/`: CNAME, logo, favicons, `admin/`.
- `themes/hextra`: copy of the release pinned in `.github/theme-pin.json`, not a submodule. Never edit; update via `scripts/vendor_theme.py`.
- `import*/`: scraped source, one level up, never committed.

## Forms
Web3Forms (Contact, Membership; each to its own mailbox) live in `hugo.toml`, `layouts/_partials/webform.html` and `layouts/page/contact-form.html` — never in content/, so Sveltia CMS can't break them. Same for new forms.

## Invariants
- `static/CNAME` exactly `www.fottp.org.uk`.
- Never commit `public/`, `resources/_gen/`, `.hugo_build.lock`.
- DNS/email at Fastmail (gruntfutuk) — don't suggest Cloudflare.
- No contact details in plain text sitewide or in content/ — use the forms.
- `git fetch`/`pull --rebase` before pushing; expect concurrent CMS/gruntfutuk commits on main; read the diff first.

## Conventions
- Small commits, plain-English messages.
- After layout/theme/Hugo changes: `hugo --minify --logLevel warn` prints nothing; check the phone menu on every page type.
- Ask before adding third-party services.
- Verify photo/fact provenance: no stock photos as real, no unconsented child photos, no uncertain archive dates/affiliations — confirm with gruntfutuk.

## Unconfirmed — don't publish
- Queen's Award year (2016 vs June 2020).
