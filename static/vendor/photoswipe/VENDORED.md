# PhotoSwipe (vendored)

The lightbox used on the gallery pages (`layouts/gallery/`). It is copied here, not loaded from a CDN, so the site
stays self-hosted. Please don't edit these files; update by replacing them as below.

- **Project:** PhotoSwipe, https://photoswipe.com, https://github.com/dimsemenov/PhotoSwipe
- **Version:** 5.4.4 (npm package `photoswipe`), licence MIT (see `LICENSE`), no other dependencies
- **Taken from:** the package tarball https://registry.npmjs.org/photoswipe/-/photoswipe-5.4.4.tgz, whose SHA-1
  (`e045dc036453493188d5c8665b0e8f1000ac4d6e`) matched the value the npm registry publishes
- **Files (from the package's `dist/`):** `photoswipe.esm.min.js`, `photoswipe-lightbox.esm.min.js`, `photoswipe.css`

## Updating

1. Look up the newest version and its tarball: `https://registry.npmjs.org/photoswipe/latest`.
2. Download the tarball, check its SHA-1 against the `dist.shasum` in that response, and unpack it.
3. Copy the three files above and `LICENSE` over the ones here, and update the version and checksum in this note.
4. Run `hugo --minify`, then open a gallery page, click a photo, and check the arrows, the Esc key, swipe on a phone
   and the caption all still work.
