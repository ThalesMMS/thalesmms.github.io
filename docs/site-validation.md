# Site validation

Reviewed November 2, 2026. The site has 17 project sections and 54 HTML pages, including root, 404 and the macOS App Store data collection declaration.

## Project review

The local inventory covers all five reachable site revisions that change project pages, with 17 project identities, 58 source entries and 42 Git working trees. Source entries include separate applications, development checkouts and embedded packages; they are not 58 released products. Product repositories were read-only.

Detailed source mappings, revisions, local changes, file hashes and findings are in the ignored `.site-work/project-inventory.json` and `.site-work/project-audit.md`. Repeat the inventory using the command in the README. The [project review](project-review.md) summarizes the public-facing changes.

Descriptions now distinguish separate implementations and release lines. AutoComp uses a JSON source instead of retaining old HTML bodies. Description review dates and privacy effective dates are independent.

## Automated checks

`python3 tools/check_site.py` passed for all 54 pages and 765 links. It checks:

- Required routes, balanced tags, unique IDs, one title, h1 and main landmark per page.
- Language, viewport metadata, labelled navigation, heading order, image attributes and skip targets.
- Internal files and fragments, active navigation and contact links.
- Local assets and absence of scripts, forms, iframes and event handlers.
- Public source-link allowlist, private-source link restrictions, local path leaks and credential patterns.
- A JSON source for every project, rendered review dates and edition guidance on presentation and support pages.

Regenerating all 54 pages produced identical HTML hashes. `git diff --check` passed. The inventory found every mapped source directory and evidence file.

## Browser checks

The updated AutoComp presentation and privacy pages, macOS IsiX presentation and Scout privacy page were loaded at the browser's 1280-pixel viewport. All four had the expected headings and dates, no missing images and no horizontal overflow. The directory was also inspected in the browser.

The earlier September review included narrow and tablet viewports. Those historical results are not a new responsive or accessibility qualification for this revision. Styles and assets did not change in this review.

## Limits

These checks verify static pages and source-derived descriptions. They do not establish app runtime behavior on every device, store availability, clinical suitability, an exhaustive security audit or third-party retention. Declared platform minimums do not prove execution on the oldest supported OS or Intel hardware.

Only the renamed public macOS repository URL was checked remotely in this review. Other projects were compared with local sources and the earlier source audit. The macOS privacy and data collection declaration remain limited to the Mac App Store edition. Separate application implementations do not inherit those declarations.

No product source, private source links, patient data or application screenshots were published. No GitHub Pages or App Store Connect settings were changed, and this local update was not pushed or deployed.
