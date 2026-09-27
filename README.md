# Friends of Telford Town Park — website

Source for [www.fottp.org.uk](https://www.fottp.org.uk): a static [Hugo](https://gohugo.io) site, using the [Hextra](https://github.com/imfing/hextra) theme, for the Friends of Telford Town Park charity. No cookies, no trackers, no third-party scripts, no CDNs.

Committee members and other authorised volunteers edit it through a web form (Sveltia CMS) or directly through Git; nothing is live until a pull request into `main` is merged.

## Working on this repo

- **Conventions** for anyone (or any tool) changing files here: [`CLAUDE.md`](CLAUDE.md).
- **Full reference** — how the site is built, editing and access, decisions and policies, open items: [`docs/HANDOFF.md`](docs/HANDOFF.md).

## Local preview

Requires [Hugo](https://gohugo.io) **extended**, 0.166.0 or newer.

```bash
hugo server
```

Open <http://localhost:1313>. Nothing here changes the live site.
