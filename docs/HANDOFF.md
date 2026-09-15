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

## Next task — content migration (in progress)
1. Run a scraper (see `scrape_old_site.py` below; place it at `D:\websites\fottp.org.uk\scrape_old_site.py`, i.e. one level above the Hugo `website` folder) that fetches each old page, converts the main content to Markdown with `markdownify`, downloads images, and writes `import/<slug>/index.md` + images + `original.html`.
2. Review and tidy the Markdown (builder HTML converts messily), then move the pages into `content/` as Hugo page bundles.
3. Commit `import/` only if useful as a record; otherwise keep it out of the repo.

Dependencies: managed as a proper **uv** project at `D:\websites\fottp.org.uk\` (not bare pip, not just a loose `.venv`) — `uv init` (creates `pyproject.toml` + `.venv`), then `uv add requests beautifulsoup4 markdownify`, then `uv run scrape_old_site.py`.

## Open decisions (not yet made)
- **Theme**: Ananke is a placeholder. Candidates discussed: Hugo Blox, Blowfish, Hextra. Choose based on what a community charity needs: image-led landing page, news/events list, static pages, easy Markdown editing.
- **Contact form**: static site needs an external form backend (Formspree / Web3Forms / Basin) or a mailto link. Not decided.
- **Analytics**: none, or a cookieless option (Plausible / GoatCounter). Aim: no cookie banner.
- **Map**: plain Google Maps iframe or OpenStreetMap embed.
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
