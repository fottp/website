# Friends of Telford Town Park (FOTTP) — public website

Hugo static site for charity FOTTP, live at https://www.fottp.org.uk, deployed via GitHub Actions to GitHub Pages. Maintainer: gruntfutuk (GitHub username; not a trustee). Read `docs/HANDOFF.md` before starting work.

**Proof-of-concept**, not a replacement, for real site https://www.fottp.co.uk (IONOS, run by a current trustee) and old WordPress archive https://friendsoftelfordtownpark.org (being harvested via its REST API). Both read-only — not ours to change. Full history in HANDOFF.md.

## Environment
- Windows native (PowerShell/Git Bash); others use GitHub Desktop+VS Code or Sveltia CMS (`/admin/`) — keep toolchain simple for both.
- Hugo **0.166.0 extended**, pinned in `.github/workflows/hugo.yml` — bump local and CI together.
- Python 3.14+: `int | float` unions, `collections.abc`. Use **uv** (`.venv`), not pip. Photos: resize to 1600px max edge, JPEG q~82, before committing (the build then makes smaller responsive copies itself — see HANDOFF.md "Image resizing").
- British English throughout.

## Layout
- `hugo.toml`: menu, Web3Forms keys, theme params.
- `content/`: Markdown, page bundles — images stay alongside their page, don't centralize.
- `layouts/`: theme overrides (see Forms). `static/vendor/`: self-hosted, no CDNs. `static/css/custom.css`: theme's override point. `static/admin/`: Sveltia CMS.
- `themes/hugo-universal-theme`: git submodule — `git submodule update --init` after clone.
- `import/`, `import-friendsoftelfordtownpark/`: scraped source, one level up, not committed.

## Forms — isolated from content/
Web3Forms (the Contact and Membership forms each deliver to their own mailbox) live in `hugo.toml` + `layouts/partials/webform.html` + `layouts/page/contact-form.html`, never inline in content/, so Sveltia CMS (content/-only) can't see or break them. Follow this pattern for future forms.

## Invariants
- `static/CNAME` must be exactly `www.fottp.org.uk`.
- Never commit `public/`, `resources/_gen/`, `.hugo_build.lock`.
- DNS/email hosted at Fastmail, managed by gruntfutuk — don't suggest Cloudflare.
- Never put contact details in plain text sitewide or in content/ — route through the forms.
- `git fetch`/`pull --rebase` before pushing. A concurrent gruntfutuk/CMS commit on main is expected — read the diff before rebasing.

## Conventions
- Small, focused commits, plain-English messages.
- Ask before adding third-party services (tracking/cookie-banner concerns).
- Verify photo/fact provenance before publishing: no stock photos as real ones, no unconsented child photos, no uncertain archive dates/affiliations — confirm with gruntfutuk.

## Open (full list: docs/HANDOFF.md)
- Queen's Award year unconfirmed (2016 vs June 2020) — don't publish until confirmed.
- FOTTP's role in the Christmas/Santa Fun Run unconfirmed — don't publish it or the Midlands Air Ambulance cheque photo until confirmed.
- `friendsoftelfordtownpark.org` archive curation (Chairman's Reports, photo galleries) paused, not finished.
