# Project handover — FOTTP website rebuild

_Generated 14 September 2026 from the claude.ai planning session. Update this file as work progresses._

## Goal
Replace the charity's existing IONOS site-builder website (https://www.fottp.co.uk) with a static Hugo site at **https://www.fottp.org.uk**, maintained in Git so future committee members can edit it with GitHub Desktop and a text editor.

## Current state — infrastructure is COMPLETE and live
| Component | Detail |
|---|---|
| Domains | `fottp.org` and `fottp.org.uk` registered via DomainBox (gruntfutuk is a reseller there) |
| DNS + email | Fastmail hosts DNS and MX for both domains. gruntfutuk has full control. MX stays at Fastmail. |
| `fottp.org.uk` (primary) | Apex: A records 185.199.108-111.153, AAAA 2606:50c0:8000-8003::153 (GitHub Pages). `www` CNAME → `fottp.github.io`. Fastmail's default web A records were disabled. |
| `fottp.org` | Left on Fastmail default web records; Fastmail "website redirect" sends it (302) to https://www.fottp.org.uk |
| GitHub | Organisation **fottp** (2FA enforced; verified domains fottp.org and fottp.org.uk). Repo **fottp/website**, public. Owner: gruntfutuk's personal account. A second owner still needs adding once the committee decides who. |
| Pages | Source = GitHub Actions. Custom domain `www.fottp.org.uk`, DNS check passed, TLS issued. "Enforce HTTPS" should be ticked if not already. |
| Workflow | `.github/workflows/hugo.yml` — actions/checkout@v4 (submodules), peaceiris/actions-hugo@v3 pinned 0.166.0 extended, configure-pages@v5, upload-pages-artifact@v3, deploy-pages@v4. Both jobs green. |
| Verified | `curl -sI https://www.fottp.org.uk` → 200 from GitHub.com. Apex → 301 to www. |

Git identity: commits use the GitHub noreply address (email-privacy protection is on). Line endings: Git for Windows autocrlf default; repo stores LF.

## Old site facts (source for migration)
- https://www.fottp.co.uk — IONOS "MyWebsite Now" builder on WordPress; `server: IONOS Webserver`; domain registered 28 May 2026 via IONOS, expires 28 May 2027, registrant redacted; held by an unknown person (possibly not a charity member). Do not modify; it will be redirected or lapsed later.
- **The WordPress REST API (`/wp-json/`) is disabled** for anonymous requests — returns "wp-json is disabled". Content must be scraped from the rendered HTML.
- Pages are a handful of static ones (home, about, partners, projects, contact) plus images under `/wp-content/uploads/go-x/`. Embedded widgets: contact form, Google Maps, translator, IONOS SiteAnalytics with cookie consent — none of these need reproducing as-is.
- Bot detection may 403 non-browser user agents; a browser-like User-Agent header may be needed.

## Content migration — DONE
All 5 old-site pages have been scraped (into `import/`, not committed) and tidied into Hugo page bundles under `content/`: home (`content/_index.md`), `about-us`, `contact-us`, `our-partners`, `our-projects`. Cleanup during tidying: stripped the old site's duplicated contact-form/map-consent widget boilerplate and JS gallery "Loading..." artefacts, and dropped stock photos left over from the builder template (a stock crowd scene, plus unrelated shots of Bath and the Lake District) rather than present them as photos of Telford Town Park. Genuine team/volunteer/partner photos were kept and renamed descriptively.

Open gaps, flagged with `<!-- TODO -->` comments in the content itself:
- `content/about-us/index.md` — needs a real event photo (old one was stock).
- `content/our-projects/index.md` — one project entry ("clearing overhanging trees") needs a real photo (old one was stock); the "Gallery" section's old-site images were only ever captured as 50×67px thumbnails by a JS lightbox, so full-resolution photos need sourcing separately.
- The "200+ members / 30+ events / 100+ projects" stats on the home page are carried over from the old site and should be verified with the committee before publishing.
- Map embed is still a TODO on `content/contact-us/index.md` — see open decisions below.
- **Contact form needs a real Web3Forms access key.** The plain `[email address removed]` address was replaced with a Web3Forms-backed HTML form (chosen 2026-09-15 to stop the address being scraped/spammed; no account dashboard needed, no cookies). Sign up at web3forms.com with `[email address removed]` to get an access key, then replace `WEB3FORMS-ACCESS-KEY-HERE` in `content/contact-us/index.md`. Needed `[markup.goldmark.renderer] unsafe = true` in `hugo.toml` so the raw `<form>` HTML in that Markdown file renders.

`import/` (the raw scrape) is kept locally only, not committed — useful as a reference while tidying but not needed once `content/` is done.

Dependencies for `scrape_old_site.py`: managed as a proper **uv** project at `D:\websites\fottp.org.uk\` (not bare pip, not just a loose `.venv`) — `uv init` (creates `pyproject.toml` + `.venv`), then `uv add requests beautifulsoup4 markdownify`, then `uv run scrape_old_site.py`.

## Theme — DECIDED
Replaced Ananke with **[hugo-universal-theme](https://github.com/devcows/hugo-universal-theme)** (2026-09-15), chosen for a working responsive hamburger nav out of the box (standard Bootstrap navbar-toggler) without needing Go/Node on top of Hugo (ruled out Blowfish for that reason; ruled out Hugo Blox for its history of breaking rebrands; ruled out hugo-hero-theme for being stale since Nov 2024).

The theme pulls in jQuery, Bootstrap 3.4.1, Font Awesome and Google's Roboto webfont — all **self-hosted** under `static/vendor/` (not loaded from CDNs) to keep the no-tracking preference. `layouts/partials/headers.html` and `layouts/partials/scripts.html` override the theme's versions to point at the local copies. `layouts/index.html` also overrides the theme's default, which only renders config-driven marketing sections (carousel/testimonials/clients) and never the page's own Markdown — the override adds the missing `{{ .Content }}` block.

The top nav is configured in `hugo.toml` under `[menu]` in the same order as the old site (Home, About Us, Our Partners, Contact Us, Our Projects). All content pages carry `type: page` front matter so they use the theme's plain single-column layout (`layouts/page/single.html`) rather than its blog/sidebar layout. The theme's own `breadcrumbs.html` partial renders the front-matter title as the page's `<h1>` — content Markdown should start below that (no leading `# Heading` matching the title) to avoid duplicate H1s.

Left disabled for now (all still open decisions, see below): `enableGoogleMaps`, `enableRecaptchaInContactForm`, `params.topbar` (would otherwise show contact details in plain text sitewide, undoing the Web3Forms change). No real FOTTP logo exists yet, so `disabled_logo = true` shows the charity name as text instead — TODO: swap in a real logo image and set `disabled_logo = false`.

## Open decisions (not yet made)
- **Analytics**: none, or a cookieless option (Plausible / GoatCounter). Aim: no cookie banner.
- **Map**: plain Google Maps iframe or OpenStreetMap embed.
- **Language selector**: the old site's flag switcher is just IONOS's "Website Translator" WordPress plugin wrapping Google's client-side Website Translator widget (machine-translates the DOM on the fly, gated behind its own cookie consent) — no real translated content behind it. Deliberately not replicating this for now (adding it back would mean a third-party script and a cookie banner, against the no-tracking preference); revisit later if genuinely needed.
- **Editing workflow for non-technical members**: GitHub Desktop + VS Code, or a Git-backed CMS (Decap / Sveltia / Pages CMS). Not decided.
- **Housekeeping**: bump action versions (Node 20 deprecation warning: checkout, configure-pages, upload-artifact). Low priority; pipeline works.
- **Second GitHub org owner** to be added.
- **Old domain** fottp.co.uk: leave until the new site is agreed; then redirect or let lapse (May 2027).

## Working preferences
- Step-by-step: run one command, check output, then continue.
- British English. Python 3.14+ idioms. Windows/PowerShell commands.
- Don't move DNS off Fastmail. Don't touch the old IONOS site.

## scrape_old_site.py (reference copy)
```python
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

BASE = "https://www.fottp.co.uk/"
OUT = Path(__file__).parent / "import"
HEADERS = {"User-Agent": "Mozilla/5.0 (FOTTP content migration; contact via fottp.org.uk)"}

session = requests.Session()
session.headers.update(HEADERS)


def fetch(url: str) -> BeautifulSoup:
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


def discover_pages(home: BeautifulSoup) -> list[str]:
    urls: set[str] = {BASE}
    for a in home.select("nav a[href], header a[href]"):
        href = urljoin(BASE, a["href"]).split("#")[0]
        if urlparse(href).netloc == urlparse(BASE).netloc:
            urls.add(href)
    return sorted(urls)


def slug_for(url: str) -> str:
    path = urlparse(url).path.strip("/")
    return path.replace("/", "-") or "home"


def save_page(url: str) -> None:
    soup = fetch(url)
    slug = slug_for(url)
    page_dir = OUT / slug
    page_dir.mkdir(parents=True, exist_ok=True)

    main = soup.find("main") or soup.body
    for tag in main.select("script, style, noscript, nav, footer"):
        tag.decompose()

    for img in main.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if not src:
            continue
        img_url = urljoin(url, src)
        name = Path(urlparse(img_url).path).name
        target = page_dir / name
        if not target.exists():
            data = session.get(img_url, timeout=30)
            if data.ok:
                target.write_bytes(data.content)
        img["src"] = name

    title = (soup.title.string or slug).split("|")[0].strip() if soup.title else slug
    body = md(str(main), heading_style="ATX", strip=["span", "div"])
    body = re.sub(r"\n{3,}", "\n\n", body).strip()

    (page_dir / "index.md").write_text(
        f"---\ntitle: \"{title}\"\nsource: \"{url}\"\n---\n\n{body}\n", encoding="utf-8"
    )
    (page_dir / "original.html").write_text(str(soup), encoding="utf-8")
    print(f"saved {slug}: {title}")


if __name__ == "__main__":
    home = fetch(BASE)
    pages = discover_pages(home)
    print("pages found:", *pages, sep="\n  ")
    for url in pages:
        save_page(url)
```
