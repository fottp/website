# Project handover — FOTTP website rebuild

_Generated 14 September 2026 from the claude.ai planning session. Update this file as work progresses._

## Goal
`fottp.org.uk` is a **proof-of-concept** aiming to hold largely the same content as the charity's current definitive site, https://www.fottp.co.uk (an IONOS site-builder site built and run day-to-day by a current trustee) — but on an open-source, Git-based static-site approach, specifically so the content isn't locked away from the wider set of trustees the way it is when one person's tooling/account is the only way to edit it. Maintained in Git so committee members can edit it with GitHub Desktop and a text editor, or (as of 2026-09-15) via the Sveltia CMS at `/admin/` for non-technical editing — see below.

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
- **https://www.fottp.co.uk is the charity's current, definitive site** — IONOS "MyWebsite Now" builder on WordPress; `server: IONOS Webserver`; domain registered 28 May 2026 via IONOS, expires 28 May 2027, registrant redacted (WHOIS privacy — this doesn't mean the site is unmaintained, it's actively built and run by a current trustee). Do not modify; it will be redirected or lapsed once `fottp.org.uk` is ready to take over.
- **The WordPress REST API (`/wp-json/`) is disabled** for anonymous requests — returns "wp-json is disabled". Content must be scraped from the rendered HTML.
- Pages are a handful of static ones (home, about, partners, projects, contact) plus images under `/wp-content/uploads/go-x/`. Embedded widgets: contact form, Google Maps, translator, IONOS SiteAnalytics with cookie consent — none of these need reproducing as-is.
- Bot detection may 403 non-browser user agents; a browser-like User-Agent header may be needed.

### A third site: https://friendsoftelfordtownpark.org — old, unmaintainable, being harvested for content
Investigated 2026-09-15. This is **not** the current site and **not** what `fottp.org.uk` is replacing — it's an older site the charity can no longer maintain, and the goal is to recover any content from it worth keeping before it's lost, folding it into `fottp.org.uk` alongside what's already been migrated from fottp.co.uk.

**Platform:** WordPress 5.4.21 (outdated — 5+ major releases behind), theme "Barletta" (a commercial ThemeForest theme) + child theme, built with the SiteOrigin Page Builder plugin. Notable plugins: The Events Calendar (real calendar/events functionality, a genuine feature gap versus fottp.co.uk and the new site), Contact Form 7, Custom Facebook Feed, Photo Gallery, Social Icons, and PixelYourSite (a Facebook-pixel/tracking plugin — worth knowing given this repo's no-tracking preference).

**Hosting:** split across two providers. DNS and email are at IONOS (nameservers on IONOS's `ui-dns.*` cluster, MX at `mx00/mx01.ionos.co.uk`, SPF references IONOS). The actual website is hosted separately — the A record (`54.38.72.95`) reverse-resolves to `ns1.dawleywebdesign.email`, and the site's own code has custom plugins literally named `dwd-carousel`/`dwd-custom-func`, pointing to a local outfit called **Dawley Web Design** running their own nginx server with Let's Encrypt TLS and self-managing the WordPress install — separate from the domain/DNS/email arrangement at IONOS. This split (and the outdated WP core) is presumably why it "cannot be maintained" going forward.

**Content scale — much bigger than fottp.co.uk, and its REST API is open** (a real advantage — content can be pulled as structured JSON via `/wp-json/wp/v2/pages`, `/wp-json/wp/v2/posts`, `/wp-json/wp/v2/media` with pagination, no HTML scraping needed): **50 pages, 85 posts, 1,278 media library items** (the media count will collapse a lot once WordPress's auto-generated thumbnail/medium/large/scaled size variants per upload are deduplicated down to originals). Content is recent — includes a post modified in 2025 and a page about a Queen's Award received March 2025.

**Not yet done:** a full raw backup/export of this site's pages, posts and media hasn't been pulled yet. Given it "cannot be maintained," treat recovering a complete local copy as the priority before deciding what specifically gets folded into `fottp.org.uk`'s curated content — same pattern as the `import/` raw-scrape-then-curate approach used for fottp.co.uk.

## Content migration — DONE
All 5 old-site pages have been scraped (into `import/`, not committed) and tidied into Hugo page bundles under `content/`: home (`content/_index.md`), `about-us`, `contact-us`, `our-partners`, `our-projects`. Cleanup during tidying: stripped the old site's duplicated contact-form/map-consent widget boilerplate and JS gallery "Loading..." artefacts, and dropped stock photos left over from the builder template (a stock crowd scene, plus unrelated shots of Bath and the Lake District) rather than present them as photos of Telford Town Park. Genuine team/volunteer/partner photos were kept and renamed descriptively.

Open gaps, flagged with `<!-- TODO -->` comments in the content itself:
- `content/our-projects/index.md` — one project entry ("clearing overhanging trees") needs a real photo of that specific activity (old one was stock); the "Gallery" bullet list's named past sessions (Grange Pool, Kitchen Depot, poly tunnel, etc.) still need their own full-resolution photos — the old site's images for those were only ever captured as 50×67px thumbnails.
- The "200+ members / 30+ events / 100+ projects" stats on the home page are carried over from the old site and should be verified with the committee before publishing.

**Real photos added 2026-09-15** (gruntfutuk's own, resized to a 1600px max edge and recompressed before committing — originals were 2-8MB camera/phone files): four photos on the home page (pond/swans, a community fun run, misty pond, snow), a real "Out and about" photo on About Us (resolving that TODO), and a new "The Park We're Protecting" section on Our Projects with photos of the Abraham Darby monument, the old chimney, and a fishing lake.

Two photos needed a quick check with gruntfutuk before use, both resolved: the fun-run photo isn't a FOTTP-organised event (just something gruntfutuk photographed at a public event in the park — captioned accordingly, not attributed to FOTTP), and the Facebook-sourced snowy photo is gruntfutuk's own (downloaded via Facebook since the original Olympus file wasn't to hand) — used as-is at 1080×1080, already web-sized by Facebook's own compression.

**Map — DECIDED: OpenStreetMap.** Added 2026-09-15 to `content/contact-us/index.md` as a plain `<iframe>` embed of `openstreetmap.org/export/embed.html` — no API key, account or cookies needed, unlike Google Maps. Uses the same coordinates (52.6708325, -2.4477144) the old site's Google Maps embed used for the park.
- Map embed is still a TODO on `content/contact-us/index.md` — see open decisions below.
- **Two Web3Forms forms, split by mailbox — DONE.** The plain `[email address removed]` address was replaced with Web3Forms-backed HTML forms (2026-09-15, to stop the address being scraped/spammed). gruntfutuk runs two mailboxes handled by different people: `[email address removed]` for membership sign-ups, `[email address removed]` for general enquiries. Web3Forms ties one access key to one destination email, so there are two forms, both live with real access keys:
  - `content/become-a-member/index.md` (linked from the homepage's "Become a Member" button) → `[email address removed]`.
  - `content/contact-us/index.md` (general enquiries, team bios) → `[email address removed]`.

  Needed `[markup.goldmark.renderer] unsafe = true` in `hugo.toml` so the raw `<form>` HTML in Markdown renders. Note: Web3Forms' dashboard concept of "a form" is just a config record (name + destination email) that issues an access key — it's unrelated to the actual HTML form, which lives in our Markdown.

`import/` (the raw scrape) is kept locally only, not committed — useful as a reference while tidying but not needed once `content/` is done.

Dependencies for `scrape_old_site.py`: managed as a proper **uv** project at `D:\websites\fottp.org.uk\` (not bare pip, not just a loose `.venv`) — `uv init` (creates `pyproject.toml` + `.venv`), then `uv add requests beautifulsoup4 markdownify`, then `uv run scrape_old_site.py`.

## Theme — DECIDED
Replaced Ananke with **[hugo-universal-theme](https://github.com/devcows/hugo-universal-theme)** (2026-09-15), chosen for a working responsive hamburger nav out of the box (standard Bootstrap navbar-toggler) without needing Go/Node on top of Hugo (ruled out Blowfish for that reason; ruled out Hugo Blox for its history of breaking rebrands; ruled out hugo-hero-theme for being stale since Nov 2024).

The theme pulls in jQuery, Bootstrap 3.4.1, Font Awesome and Google's Roboto webfont — all **self-hosted** under `static/vendor/` (not loaded from CDNs) to keep the no-tracking preference. `layouts/partials/headers.html` and `layouts/partials/scripts.html` override the theme's versions to point at the local copies. `layouts/index.html` also overrides the theme's default, which only renders config-driven marketing sections (carousel/testimonials/clients) and never the page's own Markdown — the override adds the missing `{{ .Content }}` block.

The top nav is configured in `hugo.toml` under `[menu]` in the same order as the old site (Home, About Us, Our Partners, Contact Us, Our Projects). All content pages carry `type: page` front matter so they use the theme's plain single-column layout (`layouts/page/single.html`) rather than its blog/sidebar layout. The theme's own `breadcrumbs.html` partial renders the front-matter title as the page's `<h1>` — content Markdown should start below that (no leading `# Heading` matching the title) to avoid duplicate H1s.

Left disabled for now (all still open decisions, see below): `enableGoogleMaps`, `enableRecaptchaInContactForm`, `params.topbar` (would otherwise show contact details in plain text sitewide, undoing the Web3Forms change). No real FOTTP logo exists yet, so `disabled_logo = true` shows the charity name as text instead — TODO: swap in a real logo image and set `disabled_logo = false`.

## Non-technical editing — DECIDED: Sveltia CMS at /admin/
Added 2026-09-15 so committee members can edit page content through a web form instead of Git/Markdown, without needing GitHub Desktop or VS Code at all.

**How to log in:** go to `https://www.fottp.org.uk/admin/` and click "Sign In with Token". It links to GitHub's token-creation page with the right scopes pre-selected — generate a token there (needs write access to the `fottp/website` repo), paste it into the CMS, and it's saved in your browser. This avoids needing a separate OAuth app/proxy server (a third-party service CLAUDE.md would otherwise want sign-off on) at the cost of each editor doing this one-time token setup themselves. Tokens expire (90 days by default on GitHub) and need regenerating when they do.

**What's editable:** the 6 existing pages (Home, About Us, Our Partners, Our Projects, Contact Us, Become a Member) as a fixed list — title and body text, plus any images in the page's own content bundle (uploads stay alongside that page's other files, matching Hugo's existing page-bundle layout — no image reorganisation was needed for this). New page *types* aren't supported by this config; that would need a config.yml change first.

**What's deliberately NOT editable via the CMS:** the two Web3Forms forms (access keys, hidden fields) on Contact Us and Become a Member. These were moved out of `content/` entirely into `hugo.toml` (`[params.webforms]`) and `layouts/partials/webform.html` / `layouts/page/contact-form.html`, specifically so the CMS — which only ever reads/writes files under `content/` — has no path to see or break them. The CMS's Contact Us / Become a Member entries show a hint explaining the form is handled separately. See `static/admin/config.yml` for the full field config.
## Open decisions (not yet made)
- **Analytics**: none, or a cookieless option (Plausible / GoatCounter). Aim: no cookie banner.
- **Language selector**: the old site's flag switcher is just IONOS's "Website Translator" WordPress plugin wrapping Google's client-side Website Translator widget (machine-translates the DOM on the fly, gated behind its own cookie consent) — no real translated content behind it. Deliberately not replicating this for now (adding it back would mean a third-party script and a cookie banner, against the no-tracking preference); revisit later if genuinely needed.
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
