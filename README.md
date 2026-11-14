# ThalesMMS public app site

Static HTML and CSS for https://thalesmms.github.io/. The published site has no JavaScript, forms, analytics, external fonts, or runtime dependencies.

The directory includes 18 project sections. Every project has a presentation, support, and privacy page. The macOS Mac App Store edition of IsiX also has a data collection declaration. Root and custom 404 pages bring the total to 57 HTML pages.

## Preview and maintain

From the repository root:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Open http://127.0.0.1:8080/. Stop the server with Ctrl+C.

All project copy is maintained in `content/apps/*.json`. After editing it, regenerate and validate:

```sh
python3 tools/build_site.py
python3 tools/check_site.py
git diff --check
```

These commands use only the Python standard library. Generated HTML is committed, so GitHub Pages needs no build command. AutoComp now uses the same JSON source and generator as the other projects.

`reviewed_date` records a source review on the presentation page. `editions` adds version and platform differences to presentation and support pages. Privacy effective dates remain independent, so a description review does not silently change every policy date.

Shared styles are in `assets/site.css`. The AutoComp icon is the existing Safari extension asset. Eleven additional projects use their existing product icons from the source checkouts. Initials are used for DICOM-Swift, MTK, the DICOM agent suite, dicom-go, and the separate macOS IsiX section. The dicom-go example bundle uses the standard Fyne logo, which is not used as a project logo here. No application screenshots or DICOM samples are published here.

## Routes

Each base below also has `support/` and `privacy/` subpages.

| Project | Base route |
| --- | --- |
| AutoComp for Safari | `/apps/autocomp/` |
| Turing Lab | `/apps/turing-lab/` |
| Logisim Evolution Mobile | `/apps/logisim-evolution-mobile/` |
| IsiX DICOM Viewer | `/apps/isis-dicom-viewer/` |
| IsiX DICOM Viewer for macOS, GitHub and Mac App Store editions | `/apps/isis-dicom-viewer-macos/` |
| dicom-slides | `/apps/dicom-slides/` |
| DICOM-Swift | `/apps/dicom-swift/` |
| MTK | `/apps/mtk/` |
| DICOM tools for AI agents | `/apps/dicom-agent-tools/` |
| TotalSegmentator OsiriX/Horos Plugin | `/apps/totalsegmentator-plugin/` |
| RadRef | `/apps/radref/` |
| dicom-go | `/apps/dicom-go/` |
| Podcast Intelligence | `/apps/podcast-intelligence/` |
| CodeAtlas | `/apps/codeatlas/` |
| The Legend of Source - Branches of Time | `/apps/the-legend-of-source/` |
| Scout | `/apps/scout/` |
| MacPGP | `/apps/macpgp/` |
| Video Subtitler | `/apps/video-subtitler/` |

Support and privacy copy describes the inspected implementation, including platform differences and optional provider integrations. It does not assert store availability, clinical certification, or control over third-party retention. Re-audit the affected code before updating a policy for changed data handling.

The macOS presentation covers GitHub and Mac App Store editions. Its privacy and data collection pages remain restricted to the Horos-derived Mac App Store edition at `/apps/isis-dicom-viewer-macos/privacy/` and `/apps/isis-dicom-viewer-macos/data-collection/`. The existing Apple/Android IsiX policy remains at its original route and does not cover the separate Windows application.

Only approved public repositories are linked. The DICOM agent suite describes its three components but links only dicom-skill and dicom-viewer-mcp-app, as requested by the owner.

## Publication

The publishing source is the root of `main`. `.nojekyll` keeps delivery as plain static files. Pushing does not configure GitHub Pages. Pages settings and App Store Connect are outside this site's maintenance workflow.

See `docs/site-validation.md` for the local checks and their limits.

## Repeat the project inventory

`tools/inventory_projects.py` inventories every reachable local site revision and checks an explicit source map against sibling checkouts. It records Git revisions, local changes and evidence-file hashes without launching apps or making network requests:

```sh
python3 tools/inventory_projects.py \
  --map .site-work/project-map.json \
  --output .site-work/project-inventory.json \
  --markdown .site-work/project-audit.md
```

The source map and detailed report stay in the ignored `.site-work` directory because they reference private source checkouts. The map is a JSON object keyed by site slug. Each entry has `name`, `findings`, and `sources`; each source has `path` relative to the parent directory, `role`, and an `evidence` list of relative filenames. Do not include credential files. A revision or hash change identifies material to review; it does not automatically validate or rewrite product claims.
