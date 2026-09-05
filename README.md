# ThalesMMS public app site

Static HTML and CSS for https://thalesmms.github.io/. No build step, JavaScript, or external dependencies.

## Local preview

Run `python3 -m http.server 8080 --bind 127.0.0.1` from the repository root, then visit http://127.0.0.1:8080/.

## Routes

- `/` app directory
- `/apps/autocomp/` marketing
- `/apps/autocomp/support/` support
- `/apps/autocomp/privacy/` privacy
- `/404.html` fallback served by GitHub Pages for unknown paths

Shared styles and the existing AutoComp icon are in `assets/`. The icon was copied from the Safari extension's `icons/icon512.png`. Product claims were checked against that extension's source and documentation on September 5, 2026.

## Publication

Publish the root of `main` through GitHub Pages. `.nojekyll` keeps the site as plain static files. Pushing these files does not configure Pages. The owner must configure Pages separately and verify all public HTTPS routes before using them in App Store Connect.
