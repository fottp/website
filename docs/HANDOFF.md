# Project handover — FOTTP website rebuild

_Generated 14 September 2026 from the claude.ai planning session. Update this file as work progresses._

Maintained by **gruntfutuk** (GitHub username; not a trustee of the charity).

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
| Workflow | `.github/workflows/hugo.yml` — actions/checkout@v4, peaceiris/actions-hugo@v3 pinned 0.166.0 extended, configure-pages@v5, upload-pages-artifact@v3, deploy-pages@v4. Both jobs green. |
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
- **Two Web3Forms forms, split by mailbox — DONE.** The charity's plain-text email address was replaced with Web3Forms-backed HTML forms (2026-09-15, to stop the address being scraped/spammed). gruntfutuk runs two mailboxes handled by different people: a membership mailbox for membership sign-ups and a contact mailbox for general enquiries. Web3Forms ties one access key to one destination email, so there are two forms, both live with real access keys:
  - `content/become-a-member/index.md` (linked from the homepage's "Become a Member" button) → the membership mailbox.
  - `content/contact-us/index.md` (general enquiries, team bios) → the contact mailbox.

  Needed `[markup.goldmark.renderer] unsafe = true` in `hugo.toml` so the raw `<form>` HTML in Markdown renders. Note: Web3Forms' dashboard concept of "a form" is just a config record (name + destination email) that issues an access key — it's unrelated to the actual HTML form, which lives in our Markdown.

`import/` (the raw scrape) is kept locally only, not committed — useful as a reference while tidying but not needed once `content/` is done.

Dependencies for `scrape_old_site.py`: managed as a proper **uv** project at `D:\websites\fottp.org.uk\` (not bare pip, not just a loose `.venv`) — `uv init` (creates `pyproject.toml` + `.venv`), then `uv add requests beautifulsoup4 markdownify`, then `uv run scrape_old_site.py`.

## Theme — DECIDED: Hextra (switched 2026-09-19)
History: Ananke → hugo-universal-theme (2026-09-15) → **[Hextra](https://github.com/imfing/hextra)** (2026-09-19).

**Why Hextra:** MIT licensed with no visible credit needed (the previous theme's licence required a footer link to a defunct site); actively maintained (the previous theme was in maintenance mode: last commit March 2026, unreviewed pull requests, its main maintainer's last commit July 2025); ships pre-built CSS so no Node/Go is needed; and much lighter — about 26 KB of page code (gzipped) in 3 files and no font files, against about 116 KB in 16 files plus up to 488 KB of fonts. Measured on the real content: identical text on every page (checked word for word), all 374 internal links/images resolve, and **zero WCAG 2.x A/AA violations** (axe-core, all pages, desktop and phone, phone menu open) against 25 on the old theme.

**What was kept from the old look:** the green title banner, the "Follow us" bar, the logo, the footer with About/Contact/charity number, the News list with photos, the home page "Latest news" strip, the two forms (same access keys), the map, the image resizing.

**The theme is a copy in this repo, not a submodule.** `themes/hextra/` is an unmodified copy of one release (see `themes/hextra/VENDORED.md`); `.gitattributes` forces LF line endings on it. Reason: attached as a submodule, Windows Git converts the theme's line endings and breaks some of its templates (this actually happened in testing). **Never edit inside `themes/hextra/`** — the next update replaces it wholesale. Site changes go in the site's own `layouts/`, `assets/`, `data/` and `static/`, which override the theme's.

**What we override and why** (the same list is in `.github/theme-pin.json` under `overrides`):
- `layouts/baseof.html` — adds the "Follow us" bar above the navbar; page `lang` is `en-gb`, not `en`.
- `layouts/single.html`, `home.html`, `blog/single.html`, `blog/list.html` — the green banner replaces the theme's breadcrumb and page-title H1; home adds the Latest news strip; the news list shows photo thumbnails and dates; a news post shows its lead photo and a back link.
- `layouts/404.html` — the theme's own is a bare page with no navigation or title.
- `layouts/_partials/custom/footer.html` (Hextra's footer hook) — About/Contact/charity number. `layouts/_partials/favicons.html` plus the icons in `static/` — Hextra's own are Hextra-branded; ours are made from the logo.
- `data/icons.yaml` — a three-bar "hamburger" phone menu button (Hextra's has two; its own animation code already supports the extra bar).
- `layouts/page/contact-form.html`, `layouts/_partials/webform.html`, `topbar.html`, `page-banner.html`, `latest-news.html`, `news-thumb.html`, `responsive-img.html`, `layouts/_shortcodes/osm-map.html`, `layouts/_markup/render-image.html` — the site's own pieces (no theme file shadowed).
- `assets/css/custom.css` — brand colour (logo green as Hextra's primary colour), banner, top bar, forms, news, footer. Also one **accessibility fix for a Hextra flaw**: while the phone menu is closed the theme hides it from screen readers but its links can still be tabbed into; the rule hides it properly (present in Hextra's release and dev branch; recheck after updates).
- `hugo.toml` — menu items use `pageRef` (so the theme highlights the current page and its phone menu lists just these); a site-wide `[[cascade]]` turns off the "On this page" contents panel; `disableKinds` removes the unused category/tag pages; the "Follow us" links are `[[menu.topbar]]` entries whose `params.icon` names a Hextra icon.

**Gotchas learned building it:**
- Hextra's **phone menu panel lives in `sidebar.html`**, which each page layout includes. Any layout that doesn't include it (ours for the form pages and the 404 page use the phone-only mode) gets a hamburger that opens nothing. Test the phone menu on every page type after changing layouts.
- Hextra's release (v0.12.3) lacks page hooks that exist in its development branch (`custom/page-begin`, etc.); the overrides are built on the release files, not the development ones.
- Hextra styles with pre-built Tailwind, so new class names in our templates have no styling until added to `custom.css`.
- Serve a built copy with an unused port: a `hugo server` on 1313 for the real repo is easy to mistake for a test server.

**Theme upkeep.** The site is **pinned**: `.github/theme-pin.json` records the release (`tag`), the theme files we override (`overrides`) and those our code relies on (`depends_on`). A static site with a pinned theme keeps working, so updating is a decision, not a chore.
- `.github/workflows/theme-release-watch.yml` runs `scripts/check_theme_release.py` every Monday. If Hextra has published a newer release it opens **one** GitHub issue (never repeated for the same release) listing which of our overrides and dependencies changed between the pinned release and the new one, with links to the notes and the exact changes. It changes nothing else; run it by hand any time. (GitHub pauses scheduled workflows on a public repo after 60 days without activity; a manual run or any commit wakes it.)
- To update: read the issue; run `python scripts/vendor_theme.py <tag>` (replaces `themes/hextra/`); re-apply our edits to any changed override; build with `hugo --minify --logLevel warn` (expect **no warnings**); check every page at desktop and phone width and open the phone menu on each page type; set `tag` in `.github/theme-pin.json`; commit together. Hugo itself is pinned at 0.166.0 in CI — bump it deliberately, and check for deprecation warnings when you do.
- Hextra's minimum Hugo version is 0.146.0.

## Image resizing — DONE (2026-09-19)
Photos are shrunk **at build time**, so visitors download a copy that fits their screen instead of the full 1600px original. Editors and content are unaffected: they upload and insert photos as before, and the originals in Git stay as they are (still resize to ≤1600px before committing to keep the repo small).
- `layouts/_markup/render-image.html` runs for every Markdown image. A JPEG/PNG **in the page's own folder** becomes a responsive `<img>` via `layouts/_partials/responsive-img.html`; anything else (remote address, `/static` path, SVG, GIF) is output as a plain `<img>`, as before.
- `responsive-img.html` makes 480 / 800 / 1200px copies (only ones smaller than the original, never enlarged; quality 82) and offers them plus the original in a `srcset`; the browser picks one using `sizes` and the screen. `loading="lazy"` defers photos below the fold. `sizes` matches Hextra's text column (about 672px wide on desktop). The news thumbnails and lead image use the same partial (`news-thumb.html`, `blog/single.html`); thumbnails set `noOriginal` so a phone never picks the full-size file.
- **`width`/`height` attributes are the ORIGINAL's size, deliberately.** An earlier version used the smaller copy's size, and because a `width` attribute sets the displayed size, photos shrank to 800px and stopped filling the column. Don't "correct" this.
- Resized copies are generated into the built site only (cache: `resources/_gen/`, gitignored). Nothing to commit.
- Measured in Chrome (image bytes actually downloaded, before → after, whole page scrolled): on a phone the home page went 1,579 KB → 529 KB (first screen 392 KB), Our Projects 3,673 KB → 1,719 KB, the 2 news posts about half; on desktop about 30% less overall (photos there are shown near full size, so less can be saved). Layout checked pixel-for-pixel against the old build. Resized copies could be made WebP (about a third smaller again) with a `<picture>` element — not done.

## Non-technical editing — DECIDED: Sveltia CMS at /admin/
Added 2026-09-15 so committee members can edit page content through a web form instead of Git/Markdown, without needing GitHub Desktop or VS Code at all.

**Who can log in:** someone with a GitHub account (2FA on) who has accepted their invitation to the `fottp` organisation and is in the org's `editors` team, which has **Write** access to `fottp/website`.

**How to log in:** go to `https://www.fottp.org.uk/admin/` and click "Sign In with Token", then create a fine-grained token on the GitHub page it opens and paste it into the CMS (it's saved in the browser). This avoids a separate OAuth app/proxy server (a third-party service CLAUDE.md would otherwise want sign-off on) at the cost of each editor doing this token setup themselves. **The link's pre-filled form is not enough on its own** — it creates a token for the editor's *own* account with no repositories, and the CMS then says "You don't have access to the 'website' repository". Before generating, change:
- **Resource owner** → `fottp` (not the personal account).
- **Repository access** → Only select repositories → `fottp/website`.
- **Permissions** → Contents: Read and write; Pull requests: Read and write (Metadata: Read is automatic).

The org requires administrator approval for fine-grained tokens, so the token does nothing until an owner approves it (org Settings → Third-party Access → Personal access tokens → Pending requests; check it lists only `fottp/website` and those permissions). Tokens expire (set an expiry when creating one) and need regenerating and re-approving when they do. Classic tokens are also allowed by the org but are broader (all repos the account can reach), so prefer fine-grained.

_Verified 2026-09-19: a second account added to the `editors` team logged in this way._

**How an editor makes a change** (Sveltia's editorial workflow; every change is a pull request on GitHub and nothing goes live until it is published):
1. Open **Pages** or **News** in the CMS, edit an entry (or add a News post with the **+** button) and click **Save**.
2. A box appears: click **Send for review** (or **Later** to keep it as a draft).
3. Open the entry, and in the top right change **Status: In Review** to **Ready**. A **Publish** button then appears (alternatively use the Editorial Workflow board, below).
4. Click **Publish**. The pull request is merged and its branch deleted, and the site rebuilds — the change is live within a minute or two.

The **Editorial Workflow board** (Draft / In Review / Ready columns) is the branch-and-pencil icon, third from the left in the top-left corner. The icons have no hover labels. Cards can be dragged between columns, and each card offers the actions for its stage.

**Never merge a CMS pull request on GitHub itself.** Only the CMS's Publish deletes the `cms/…` branch, and a branch left behind makes the CMS think the entry is still unpublished (this happened with the first test post: the CMS said "not published yet" for a live page until the leftover branches were deleted). If it happens, delete the leftover `cms/…` branch on GitHub and hard-refresh the CMS (Ctrl+F5). As a backstop the repo now has "Automatically delete head branches" turned on (Settings → General → Pull Requests), so merged branches should tidy themselves up, but still publish through the CMS. A hard refresh is also the fix if the CMS ever seems to use an old config (e.g. it tries to save straight to `main` and errors with "Changes must be made through a pull request").

**Deleting a published entry:** per Sveltia's docs, Delete opens a pull request that removes it and the entry stays live, marked "Pending Deletion", until you use **Delete** on its card on the Editorial Workflow board (**Cancel** leaves it in place). Not yet tried here — the first test post was removed via GitHub's "Delete directory" and a normal pull request, which also works.

_Verified 2026-09-19: an editor account edited "Become a Member", sent it for review, set it Ready and published it; the pull request touched only `content/become-a-member/index.md` and the site updated within moments._

**What's editable:** the 6 existing pages (Home, About Us, Our Partners, Our Projects, Contact Us, Become a Member) as a fixed list — title and body text, plus any images in the page's own content bundle (uploads stay alongside that page's other files, matching Hugo's existing page-bundle layout — no image reorganisation was needed for this). New page *types* aren't supported by this config; that would need a config.yml change first. (The one exception is **News**, added 2026-09-19: a `news` folder collection under `content/news/`, where each post is its own page bundle. The News page, the "Latest news" strip on the home page and the RSS feed all fill in automatically from those posts; the strip stays hidden until the first post exists.)

**What's deliberately NOT editable via the CMS:** the two Web3Forms forms (access keys, hidden fields) on Contact Us and Become a Member. These were moved out of `content/` entirely into `hugo.toml` (`[params.webforms]`) and `layouts/_partials/webform.html` / `layouts/page/contact-form.html`, specifically so the CMS — which only ever reads/writes files under `content/` — has no path to see or break them. The CMS's Contact Us / Become a Member entries show a hint explaining the form is handled separately. See `static/admin/config.yml` for the full field config.
## Access and review — DECIDED 2026-09-19 (ruleset on `main` created; part of it not yet tested)
**People:** the GitHub organisation should have at least two **owners**, each a named person with their own GitHub account and 2FA (the org already enforces 2FA) — not a shared login, so the audit log shows who did what and nobody is the single point of failure. **Editors** are an org team with Write access to `fottp/website`; they sign in to `/admin/` with their own token (see above).

**Why review, not just permissions:** GitHub can't limit a Write collaborator to one folder, so an editor's account can technically change any file (layouts, `hugo.toml`, the deploy workflow). Protection therefore comes from requiring an owner's review for anything that isn't page/news content:
- `static/admin/config.yml` has `publish_mode: editorial_workflow` — each CMS save becomes a draft pull request, and "Publish" merges it.
- `.github/CODEOWNERS` makes the owners code owners of everything **except** `/content/`.
- Raw HTML is not enabled in Markdown (goldmark `unsafe` is off), so an editor can't inject scripts through content.

**Branch ruleset to create on `main`** (repo Settings → Rules → Rulesets → New branch ruleset, target: default branch): enforcement Active; bypass list = Repository admin role (so owners can still push directly); rules: restrict deletions, block force pushes, require a pull request before merging with **0** required approvals and **Require review from Code Owners** ticked. Order matters — set `editorial_workflow` live first, or editors' direct saves will be rejected. Then add the second owner to `CODEOWNERS` (a code owner can't approve their own PR).

**Status:** the ruleset requiring pull requests on `main` is active, and the content path is verified — an editor account edited, reviewed and published a page and a news post through the CMS with no approval needed, and a direct CMS save was correctly rejected before the editorial workflow was picked up.

**Verified:** owners on the ruleset's bypass list can push directly to `main` — a Git push by an owner was accepted on 2026-09-19, with GitHub logging "Bypassed rule violations for refs/heads/main: Changes must be made through a pull request". An owner's direct *CMS* save was rejected once (before the editorial workflow config had loaded), so the CMS itself is not exempt: owners editing through the CMS follow the same Save → Send for review → Ready → Publish steps as editors.

**Verified 2026-09-19 — changes outside `content/` are blocked for editors:** an editor account edited `docs/HANDOFF.md` on github.com. GitHub put the edit on a new branch rather than `main`, and the resulting pull request showed "Review required — Code owner review required by reviewers with write access" and "Merging is blocked — waiting on code owner review", with the code owner automatically requested as reviewer. The test pull request was closed unmerged and its branch deleted.

**Still only indirectly confirmed:** that an editor's *direct push* to `main` is rejected — GitHub's web editor diverted the edit to a new branch, which is what it does for an account that can't write to a protected branch, but no push was actually attempted and refused.

**Gotcha:** the REST API's `mergeable_state` read `clean` for that blocked pull request when queried without logging in, so don't use it to judge whether the review rule is working; check the pull request page as a logged-in user.

### Role-based accounts and handover (general pattern)
Where a job belongs to a committee role rather than a person (secretary, treasurer…), an account can be named for the role and handed on, so access follows the role and no one person's own account becomes a single point of failure. It works for any service, not just GitHub: an **editor** account for the role, tied to a role mailbox on the charity's own domain (the address itself deliberately isn't listed here — this repo is public), used by **one person at a time — never shared between people**.

**Rules**
- **Least privilege:** role accounts are for editing (the `editors` team), never organisation owners. Owners are always named individuals (see People above).
- **The mailbox is the recovery route,** so it must deliver to the current role holder and ideally also to a second trustee, so a lost phone or forgotten password isn't a lock-out.
- **The current holder controls the security details:** their own 2FA device and their own password. Recovery codes are kept somewhere the charity controls (the charity's password manager, or held by a second trustee), not only on the holder's phone.
- **Tokens always have an expiry** (and, for GitHub, an owner approves each one), so a forgotten token stops working by itself.
- **Check the service's terms:** GitHub's are strict about one person per account, which is why a role account must have exactly one holder at a time.

**Handover checklist** (when the role passes to someone new)
1. *Outgoing holder:* tell a second trustee/owner; revoke any personal access tokens (GitHub → Settings → Developer settings) and sign out other sessions.
2. *Mailbox:* point the role address at the new holder (and keep the second trustee on it).
3. *Incoming holder:* sign in via "forgot password" from the mailbox and set a new password; set up 2FA on their own device, remove the old device and generate fresh recovery codes, storing them as above.
4. *Incoming holder:* create a new fine-grained token (resource owner `fottp`, repo `website`, Contents and Pull requests: Read and write, with an expiry).
5. *An org owner:* approve the new token and revoke the old one (org Settings → Third-party Access → Personal access tokens), and check the account is still in the `editors` team and nothing else.

## Events — DONE (2026-09-20)
One page bundle per event under `content/events/<name>/index.md`, added and edited through the "Events" collection in Sveltia CMS (or as files). No third-party services, cookies or JavaScript.

**Front matter:** `title`, `start` (`2026-10-10 11:00`, London time), optional `end`, `location` (default "Telford Town Park", set in `hugo.toml` `[params.events]`), `cost`, `description`, `image`/`image_alt`, `link_url`/`link_label`, and for weekly events `repeats: weekly`, `until`, `skip_dates`. A `start` with no time and no `end` time is shown and sent to calendars as an all-day event.

**Weekly events** (currently just `wednesday-volunteering`): `start`/`end` are the *first* session; every later one is the same time a week on, so the clock time stays put across the summer-time changes. `skip_dates` removes a session (bank holiday), `until` ends the series. Only weekly repeats are supported; monthly would mean extending `layouts/_partials/events/occurrences.html` and the `RRULE` line in `ics-event.html`.

**What it produces:** the Events page (`/events/`: upcoming, every week, past), a "Coming up" strip on the home page (next three; a weekly event counts once), an event page each with structured data for search engines, and calendar files: `/events/index.ics` (everything coming up, for subscribing) and `/events/<name>/index.ics` (one event, "Add to your calendar"). Templates are in `layouts/events/` and `layouts/_partials/events/`.

**Nightly rebuild:** the site is static, so "upcoming" and "past" are only worked out when it is built. `.github/workflows/hugo.yml` therefore also runs at 00:20 UTC every night; without it a finished event would stay listed until the next edit. GitHub pauses scheduled runs after 60 days with no activity on a public repo — any push (including a CMS edit) restarts them. The same rebuild makes a future-dated news post appear on its day.

**Not yet checked:** the Events form in Sveltia CMS itself (the config parses, but datetime fields, the weekly `select` and the skipped-dates list haven't been tried in the live `/admin/`), and the phone menu on the new pages. The old WordPress site's six events (2016–2018) were not imported.

## Open decisions (not yet made)
- **Analytics**: none, or a cookieless option (Plausible / GoatCounter). Aim: no cookie banner.
- **Language selector**: the old site's flag switcher is just IONOS's "Website Translator" WordPress plugin wrapping Google's client-side Website Translator widget (machine-translates the DOM on the fly, gated behind its own cookie consent) — no real translated content behind it. Deliberately not replicating this for now (adding it back would mean a third-party script and a cookie banner, against the no-tracking preference); revisit later if genuinely needed.
- **Housekeeping**: bump action versions (Node 20 deprecation warning: checkout, configure-pages, upload-artifact). Low priority; pipeline works.
- **Second GitHub org owner** to be added.
- **Old domain** fottp.co.uk: leave until the new site is agreed; then redirect or let lapse (May 2027).
- **Queen's Award for Voluntary Service — year unconfirmed.** One archive page implied 2016, another June 2020 (possibly awarded twice). About Us names the award with no year; don't publish a specific year until gruntfutuk confirms.
- **Christmas/Santa Fun Run — FOTTP's role unconfirmed.** A 2012 archive post (for RNIB/Guide Dogs) suggests FOTTP ran it, but gruntfutuk wasn't aware of this either. Don't publish it, and don't use the linked Midlands Air Ambulance cheque photo, until confirmed.

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
