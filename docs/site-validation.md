# Local site validation

Validated September 5, 2026 before publication.

- All five HTML pages parsed with balanced tags, one h1, English language, viewport metadata, unique IDs, image alt attributes, and resolvable internal links and fragments.
- Local HTTP server returned 200 for all five routes, shared CSS, and the icon.
- In-app browser rendered the home and marketing pages at desktop width. All five pages fit a 320px viewport without horizontal overflow and loaded their images.
- Keyboard Tab reached the visible Skip to content link with a solid focus outline. Semantic navigation, headings, main, and footer were inspected. This was a basic accessibility review, not a full screen-reader audit.
- Main text/link color pairs exceeded 4.5:1 contrast. The lowest tested pair was muted body text on the page background at 6.13:1.
- No script, form, or iframe elements. All styles and images are local. Page content and navigation require no JavaScript.
- Credential-pattern scan of repository text found no private-key blocks, GitHub tokens, OpenAI-style keys, or AWS access key IDs. Authored content was reviewed and contains no actual credentials or patient records.
- The icon matches the Safari extension's icons/icon512.png byte for byte.
- Product statements were checked against the Safari extension README, manifest, background request code, shared context limits, and trusted IndexedDB storage implementation.
- Git diff whitespace validation passed.

GitHub Pages settings and App Store Connect were not changed. Public HTTPS route availability remains to be checked after the owner configures Pages. A plain Python server serves /404.html directly; GitHub Pages supplies the custom fallback behavior for unknown routes.
