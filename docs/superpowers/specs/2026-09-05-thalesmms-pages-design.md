# ThalesMMS public app site

## Goal

Create a public, static GitHub Pages site at `https://thalesmms.github.io/` for app marketing, support, and privacy links that can be entered in App Store Connect. Keep the existing `ThalesMMS/ThalesMMS` profile repository unchanged.

## Scope

- Repository: `ThalesMMS/thalesmms.github.io`.
- Publishing source: the `main` branch root, using plain static files and no server-side runtime.
- Initial product coverage: AutoComp for Safari.
- Future products can be added under the same `/apps/<slug>/` namespace without changing the site domain.
- The site will not contain API keys, credentials, patient data, private build artifacts, forms, analytics, or third-party tracking scripts.

## URL structure

- `/` — personal app directory and site landing page.
- `/apps/autocomp/` — AutoComp marketing page.
- `/apps/autocomp/support/` — support, setup guidance, troubleshooting, and contact email.
- `/apps/autocomp/privacy/` — AutoComp privacy policy and endpoint-data explanation.
- `/404.html` — clear fallback page with links back to the app directory.

The App Store Connect values will be:

- Support URL: `https://thalesmms.github.io/apps/autocomp/support/`
- Marketing URL: `https://thalesmms.github.io/apps/autocomp/`
- Privacy Policy URL: `https://thalesmms.github.io/apps/autocomp/privacy/`

## Content and visual direction

Use English as the initial site language to match the current App Store Connect primary localization. Keep the copy factual and product-oriented: AutoComp provides inline autocomplete in Google Docs, uses a user-configured OpenAI-compatible HTTPS endpoint, and has no developer-hosted account or analytics service. The support page will identify Thales Matheus M Santos and `thalesmmsradio@gmail.com` as the contact. The privacy page will distinguish the app's behavior from the retention and privacy practices of the endpoint provider selected by the user.

Use the existing AutoComp icon as the primary visual asset, a restrained blue palette derived from that icon, readable system typography, responsive layout, visible keyboard focus, and no external font or JavaScript dependency. Shared navigation will link Home, AutoComp, Support, and Privacy. Pages must remain usable without JavaScript.

## Deployment and verification

1. Add the static pages and assets to the repository.
2. Validate HTML structure, internal links, absence of secrets, and responsive behavior locally.
3. Commit and push the site to `main`.
4. Configure GitHub Pages to deploy from `main` and `/`.
5. Verify the live root and all AutoComp routes over HTTPS before entering them in App Store Connect.

The implementation will pause before the GitHub Pages settings “Save” action so the owner can review and confirm the publication configuration.

## Acceptance criteria

- `https://thalesmms.github.io/` and all three AutoComp routes return the intended page over HTTPS.
- Support includes a working `mailto:` contact link and setup/troubleshooting guidance.
- Marketing explains the product without promising an included AI provider or account service.
- Privacy policy accurately describes user-configured endpoint transmission and avoids claiming control over third-party retention.
- No secrets or user/patient data are present in the site repository or generated pages.
- The existing profile repository and its README remain untouched.
