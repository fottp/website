# Friends of Telford Town Park (FOTTP) — public website

Hugo static site for the registered charity "Friends of Telford Town Park (FOTTP)".
Live at https://www.fottp.org.uk, built and deployed by GitHub Actions to GitHub Pages.
Maintainer: gruntfutuk (GitHub username; not a trustee). Read `docs/HANDOFF.md` for full project state before starting work.

This site is a **proof-of-concept**, not a replacement for an abandoned site. The charity's real, current site is https://www.fottp.co.uk (IONOS site-builder, built and run day-to-day by a current trustee). fottp.org.uk aims to hold largely the same content via an open, Git-based static-site approach so it isn't locked to one trustee's tooling/account. A third site, https://friendsoftelfordtownpark.org, is an old WordPress install the charity can no longer maintain — content is being harvested from it (via its open REST API) into this site; see `docs/HANDOFF.md` for the full three-site history and what's been migrated so far.

## Environment
- Developed on native Windows (PowerShell / Git Bash). Other charity members use GitHub Desktop + VS Code, or the Sveltia CMS at `/admin/` (no Git needed at all) — keep the toolchain simple for both paths.
- Hugo **0.166.0 extended** (winget `Hugo.Hugo.Extended`). Version pinned in `.github/workflows/hugo.yml`; bump local and CI together.
- Python 3.14+ for helper scripts: `int | float` unions, `collections.abc`, not `typing`. Manage with **uv** (local `.venv`, not bare `pip`). For one-off image work, `uv run --with pillow python ...` is fine without adding Pillow to a project. Convention for photos added to the site: resize to a 1600px max edge, JPEG quality ~82, before committing — originals are typically several MB.
- British English spelling throughout content and copy.

## Layout
- `hugo.toml` — site config: `[menu]` (the 5-item nav, order matches the old site), `[params.webforms.*]` (Web3Forms access keys — see **Forms** below), theme/logo/topbar params.
- `content/` — Markdown pages, edited directly or via the Sveltia CMS. Images live alongside their own page (Hugo page bundles) — the CMS is configured for this (entry-relative media folders per collection), so don't centralize images into one shared folder.
- `layouts/` — small, deliberate overrides of the theme (see **Forms**); `static/vendor/` — self-hosted jQuery/Bootstrap/Font Awesome/Roboto (no CDNs, per the no-tracking preference); `static/css/custom.css` — the theme's own designated override point (currently fixes images overflowing the viewport on mobile); `static/admin/` — the Sveltia CMS (`index.html` + `config.yml`).
- `themes/hugo-universal-theme` — git **submodule**. Run `git submodule update --init` after a fresh clone.
- `.github/workflows/hugo.yml` — build (`hugo --minify`) and deploy to Pages on push to `main`.
- `import/` and `import-friendsoftelfordtownpark/` — raw scraped content from the two old sites, kept as siblings of this repo (one level up in `D:\websites\fottp.org.uk\`), **not** committed. See `scrape_old_site.py` and `scrape_friendsoftelfordtownpark.py` there.

## Forms — deliberately isolated from content/
The two Web3Forms forms (Contact Us → `[email address removed]`, Become a Member → `[email address removed]`) are **not** written into their Markdown files. Access keys live in `hugo.toml` (`[params.webforms.contact]` / `[params.webforms.membership]`), the actual `<form>` markup in `layouts/partials/webform.html`, rendered automatically by `layouts/page/contact-form.html` for any page whose front matter sets `layout: contact-form` + `webform: <name>`. This means the Sveltia CMS — which only ever reads/writes files under `content/` — has no path to see or break the forms. Follow the same pattern (config + layout, not inline content) for any future form.

## Invariants — do not break
- `static/CNAME` must contain exactly `www.fottp.org.uk`.
- Never commit `public/`, `resources/_gen/` or `.hugo_build.lock` (see `.gitignore`).
- DNS and email for fottp.org / fottp.org.uk are hosted at Fastmail and managed by gruntfutuk — do not suggest moving DNS to Cloudflare.
- Never put an email address or other contact detail in plain text anywhere that renders sitewide or in `content/` (e.g. the topbar, an HTML comment) — that's exactly what the Web3Forms migration was meant to stop. Route contact through the forms instead.
- `git fetch` / `pull --rebase` before pushing to this repo. gruntfutuk now edits live via the Sveltia CMS, so a concurrent commit on `main` (author shows as their GitHub identity, message like `Update Pages "<name>"`) is expected, not a conflict to be alarmed by — read the diff before rebasing so nothing gets silently overwritten.
- The real site (https://www.fottp.co.uk) and the old archive (https://friendsoftelfordtownpark.org) are not ours to change — read-only source material only.

## Conventions
- Small, focused commits with plain-English messages.
- Ask before adding third-party services (form backends, analytics, CDNs, OAuth proxies); the charity wants minimal tracking and no cookie banner if avoidable — this is why vendor assets are self-hosted and the CMS uses a personal-access-token login rather than a separate OAuth proxy app.
- Check image and fact provenance before publishing: don't present stock/inherited photos as real park photos, don't publish identifiable photos of children without known consent, and don't assert uncertain dates/event affiliations pulled from old archives — verify with gruntfutuk first.

## Outstanding / open
See `docs/HANDOFF.md` for the full, current list (theme/analytics/map decisions, specific photos still needed, second GitHub org owner, old-domain wind-down). As of 2026-09-16, also specifically open:
- **Queen's Award for Voluntary Service year is unconfirmed** — one archive page implied 2016, another implied June 2020 (possibly awarded twice). Don't publish a specific year until gruntfutuk confirms.
- **Whether FOTTP historically ran the Christmas/Santa Fun Run** (for RNIB/Guide Dogs, per a 2012 archive post) is unconfirmed — gruntfutuk wasn't aware of this either. Don't publish it, and don't use the linked Midlands Air Ambulance cheque photo, until confirmed.
- Further curation of the `friendsoftelfordtownpark.org` backup (Chairman's Reports/governance history, remaining photo galleries) was paused, not finished — see the "Non-technical editing" / archive sections of `docs/HANDOFF.md`.
