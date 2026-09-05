# Site validation

Validated September 5, 2026 for the directory expansion.

## Coverage

- 15 new project sections, each with presentation, support, and privacy pages.
- 50 HTML pages total, including the three existing AutoComp pages, root, and 404.
- Source review covered the requested projects, both Apple and Android Isis implementations, and each component of the DICOM agent suite. Product source checkouts were read-only.
- Separate factual and site-structure reviews found no actionable defects. AutoComp's product copy was preserved from its earlier review.

## Automated checks

`python3 tools/check_site.py` passed for all 50 pages and 704 links. It checks:

- Required routes, balanced tags, unique IDs, one title, h1 and main landmark per page.
- English language, viewport metadata, labelled navigation, heading order, image attributes, and skip-link targets.
- Internal files and fragments, project-specific active navigation, and support/privacy contact links.
- Local runtime assets, no script/form/iframe elements or inline event handlers.
- A public-source URL allowlist, empty repository lists for closed projects, no local filesystem paths in public copy, and credential patterns.

Regenerating the site produced identical HTML hashes. All three AutoComp main content bodies match the previous committed version exactly. `git diff --check` passed.

## Browser checks

- All 50 pages were loaded at 320, 768, and 1280 CSS pixels: 150 layout checks, no horizontal overflow.
- Images loaded; each page had one h1 and one main landmark. The tablet/desktop checks found no page scripts.
- Activating Skip to content with the keyboard moved focus to main.
- Visual review covered the directory, category cards, and a long project name on a narrow privacy page.
- Shared text colors retain contrast ratios above 4.5:1; the lowest reviewed text pair is muted text on the page background at 6.13:1.

## Content and privacy boundaries

- Code-grounded copy distinguishes local data, external providers, settings/credentials, exports, and deletion limits.
- Libraries describe their own behavior and the responsibilities of host applications.
- TotalSegmentator copy includes Python usage reporting and the selected-runtime caveat.
- No private source links, source excerpts, user media, patient records, or DICOM sample assets were added. The existing AutoComp icon is retained.
- The private dicom-plugin repository link is omitted with the owner's confirmation; the suite still describes all three components.
- Support uses Thales Matheus M Santos and thalesmmsradio@gmail.com throughout.

## Limits

These checks verify static pages and source-derived descriptions. They are not clinical validation, an exhaustive security audit, screen-reader certification, or runtime validation of every application and external service. Third-party retention is not controlled by this site.

No GitHub Pages settings or App Store Connect settings were changed. Local /404.html can be checked directly; custom handling of an unknown path is provided by GitHub Pages when deployed.

## Product icon correction

Eleven original product icons were added to the directory, presentation, support, privacy, and favicon rendering. Source PNGs were copied unchanged and visually inspected. Together with AutoComp, 12 project sections now use product artwork. DICOM-Swift, MTK, the DICOM agent suite, and dicom-go retain initials because no own product icon was found in their current checkouts. The dicom-go example app contains the standard Fyne framework icon.

The icon correction passed static validation for 50 pages and 704 links. All 11 added source PNGs match byte for byte; their declared dimensions match the files. All 49 catalog/project pages were loaded at 320 CSS pixels with no missing images or horizontal overflow.
