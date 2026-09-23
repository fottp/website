---
title: "How This Website Works"
type: page
sidebar:
  exclude: true   # keep out of the phone menu, which should list only the 8 main pages
description: "A behind-the-scenes look at how the Friends of Telford Town Park website is built, hosted, and kept running."
draft: false
---

{{< callout type="warning" >}}
**You're looking at a preview.** This is a possible new website for Friends of Telford Town Park (FOTTP) — it is not yet the charity's official site. It's currently being reviewed by the FOTTP committee and may change.
{{< /callout >}}

We're often asked how the website is put together and where it "lives", so here's an explanation — starting in plain English, with more technical detail further down for anyone who wants it.

## In short

This website is a set of simple web pages, automatically assembled from plain text files and published to the internet using GitHub, a well-known, free hosting service used by millions of software and website projects worldwide. There's no traditional database and no server for a committee member to maintain — updates are made through an easy, browser-based editing tool, and the live site rebuilds itself automatically within a couple of minutes of any change being saved. The photo gallery, archive of past documents, news and events are all part of the same site, built the same way — nothing is hosted separately or bolted on from elsewhere.

We also keep independent backup copies of the site's content and its full history, maintained separately from the main hosting, so the website isn't dependent on any single company or service continuing to work.

## How updates get published

1. **Editing** — Committee members and other volunteers who have been given authorised access make changes using a straightforward, browser-based content editor. No coding knowledge or special software is needed.
2. **Review** — Each change goes through a short review step before it's published, and is recorded as a discrete, timestamped entry in a version-control system that keeps a complete history of every edit ever made — so nothing is ever permanently lost, and any change can be reviewed or reversed.
3. **Building** — Publishing a change automatically triggers a build process that turns the underlying text files, and any photos or documents attached to them, into the finished web pages you see.
4. **Publishing** — The finished pages are automatically published to the live site, typically within a minute or two. The site also rebuilds itself automatically every night, so that dates — "upcoming" versus "past" events, for instance — are always current even if nobody has made any edits.

## Where things live

| Component | What it does |
|---|---|
| **Domain name** (fottp.org.uk) | Registered through a UK domain registrar and points to our web hosting via standard DNS records |
| **Website hosting** | GitHub Pages — free to use, part of GitHub (owned by Microsoft) |
| **Visual design (theme)** | Hextra — free, open-source software, chosen in part for its strong accessibility record, adapted with our own colours, layout tweaks and page types |
| **Content editor** | Sveltia CMS — free, open-source software; a lightweight, browser-based editing tool that writes directly into the site's version-controlled files, so there's no separate database to manage or lose |
| **Version control** (the record of every edit) | Git — a free, open-source, and openly standardised system used to track changes, which underpins the content editor, the backups and the mirrors described below |
| **Photo gallery, archive & events** | Built directly into the site itself using the same tools as everything else — not hosted or maintained separately. The gallery's photo viewer is PhotoSwipe — free, open-source software |
| **Automated build & publish** | GitHub Actions — free to use, part of GitHub; rebuilds and republishes the site automatically whenever content changes, and every night regardless |
| **Backups & mirrors** | Forgejo — free, open-source software; independent copies of the site's full source and history are kept here, on infrastructure maintained by our IT volunteer, separate from the main hosting provider |

## Keeping the site resilient

The live site depends on one hosting provider, which is reliable but not something the charity controls directly. To reduce that dependency:

- The complete source and edit history of the site is mirrored to [Forgejo](https://forgejo.org/) — an open-source, self-hosted alternative to GitHub — running on infrastructure our IT volunteer maintains independently of the main hosting provider.
- A standby copy of the built website is also kept up to date on separate infrastructure, so a working version of the site could be brought back online elsewhere at short notice if the primary host were ever unavailable.

## Who can make changes

Access to edit the website is restricted to committee members and other volunteers who have each been individually authorised, with their own login approved by the organisation's account owners. Access to the underlying technical infrastructure (hosting accounts, source repository, DNS) is limited to the IT volunteer role.

## Accessibility

The visual design was chosen carefully with accessibility in mind, including for visitors who use screen readers or other vision-support technology, and every photograph on the site has "alt text" describing what it shows. Full details, including where we currently fall short, are on our [Accessibility Statement](/accessibility-statement/) page.

## Privacy by design

No contact details appear anywhere on the site as plain text — enquiries go through the site's own contact forms instead, to discourage automated harvesting. The site uses no cookies, no visitor tracking or analytics, and no third-party scripts or content-delivery networks beyond the hosting platform itself. What happens to the data you do send us, through those forms, is covered on our [Privacy & Cookies](/privacy-and-cookies/) page.

## Data and hosting location

No confidential or sensitive personal information is published on this public website. Most of the hosting and automation services we use — GitHub chief among them — are, like the overwhelming majority of services used by UK charities, businesses and public bodies, run by companies with a base of operations in the United States. The service behind our two forms is the exception: it's a small server we run ourselves, hosted in the UK, which sends submissions on by email through Fastmail — the same provider that already runs the charity's other email and this site's domain, not a new company. Either way, this means the data involved could, in principle, be subject to US as well as UK/EU legal frameworks, in addition to wherever the physical servers happen to sit. Because everything on this site is intended to be public, this has no practical effect on what's published here. Our approach to genuinely confidential material — committee papers, correspondence, and similar — is handled through separate arrangements, not covered by this page.

## For the technically curious

- **Static site generator:** [Hugo](https://gohugo.io/) (extended edition) — free, open-source software, version pinned for consistent builds
- **Theme:** [Hextra](https://github.com/imfing/hextra) (MIT-licensed), a vendored, version-pinned copy with our own overrides layered on top rather than edited in place — chosen partly for a clean accessibility audit result (zero WCAG 2.x A/AA violations found in testing) and a small code footprint
- **Hosting:** GitHub Pages — free to use
- **CI/CD:** GitHub Actions — free to use (within its included allowance); builds on every content push, plus a nightly scheduled rebuild so date-dependent content (events, news) stays accurate
- **Content management:** [Sveltia CMS](https://github.com/sveltia/sveltia-cms) — free, open-source software; a Git-backed headless CMS working through an editorial review step — content edits are committed directly to the repository, with no separate database layer
- **Version control:** Git — free, open-source, and an open standard in its own right; hosted on GitHub. The repository's visibility (public or private) may vary over time — currently public, since GitHub Pages on the free tier requires this — but the workflow described here is unaffected either way. A published site stays public regardless of whether its source repository is public or private
- **Forms:** a small relay we wrote and host ourselves, replacing a third-party service we used at first — plain [Python](https://www.python.org/), using only its own standard library, so nothing is pulled in from anyone else's code and there's nothing for a dependency-vulnerability scanner to ever need to flag. It runs on a small free-tier server we host in the UK, with [Caddy](https://caddyserver.com/) (MIT-licensed, open source) handling HTTPS in front of it, and forwards each submission on by email through Fastmail rather than storing it. It's a small, self-contained piece of the site — just two forms — so it could be changed again without touching anything else
- **Map:** an OpenStreetMap embed, with no API key, account or cookies required
- **Photo gallery:** a section of the same Hugo site, with a lightbox viewer via [PhotoSwipe](https://photoswipe.com/) (MIT-licensed, vendored locally rather than loaded from elsewhere)
- **Images:** automatically resized into multiple resolutions and converted to modern formats at build time, so visitors never download a full-size original unnecessarily
- **DNS:** the domain's DNS records point to GitHub Pages; these are standard, publicly resolvable records that can be checked independently with tools such as `dig`, `nslookup`, or any online DNS lookup service
- **TLS/HTTPS:** certificates are issued and renewed automatically by the hosting platform
- **Redundancy:** the repository is mirrored to [Forgejo](https://forgejo.org/) — a fully open-source, self-hosted Git platform comparable to GitHub — and a parallel build pipeline produces a standby copy of the site on independent hosting

## Questions

If you have questions about how the site works, or would like to get involved in maintaining it, please get in touch via our [contact page](/contact-us/).
