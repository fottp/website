# FlexSearch (vendored)

The client-side search index used by the theme's search box (`hugo.toml` `[params.search]`,
`themes/hextra/layouts/_partials/scripts/search.html`). Copied here, not loaded from a CDN
(the theme's default), so the site stays self-hosted and no third-party request happens when
someone searches. It lives under `assets/` rather than `static/vendor/` (unlike PhotoSwipe)
because the theme loads it through Hugo Pipes (`resources.Get`) to fingerprint it and add a
Subresource Integrity hash — that only works for files under `assets/`. Please don't edit this
file; update by replacing it as below.

- **Project:** FlexSearch, https://github.com/nextapps-de/flexsearch
- **Version:** 0.8.143 (npm package `flexsearch`), licence Apache-2.0 (see `LICENSE`), no other
  dependencies. Matches the version the theme's default CDN path uses, so it stays within what
  upstream has tested.
- **Taken from:** the package tarball https://registry.npmjs.org/flexsearch/-/flexsearch-0.8.143.tgz,
  whose SHA-1 (`b74069a933118b5e07a7e6fc6e073c6705775b65`) matched the value the npm registry publishes
- **File (from the package's `dist/`):** `flexsearch.bundle.min.js` — the same file the theme's
  default CDN path (`flexsearch.bundle.min.js` under jsdelivr) would otherwise fetch at build time

## Updating

1. Look up the newest version and its tarball: `https://registry.npmjs.org/flexsearch/latest`.
2. Download the tarball, check its SHA-1 against the `dist.shasum` in that response, and unpack it.
3. Copy `dist/flexsearch.bundle.min.js` and `LICENSE` over the ones here, and update the version and
   checksum in this note. Also update `params.search.flexsearch.version` in `hugo.toml` if set, so the
   two stay in sync even though the version param isn't used for fetching once this asset path is set.
4. Run `hugo --minify --logLevel warn`, then open any page, press `/` or Ctrl+K, and check results,
   arrow-key navigation, Enter and Escape all still work, and a screen reader announces the result count.
