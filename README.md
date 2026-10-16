# ThalesMMS public app site

Static HTML and CSS for https://thalesmms.github.io/. The published site has no JavaScript, forms, analytics, external fonts, or runtime dependencies.

The directory includes 17 project sections. Every project has a presentation, support, and privacy page. The macOS Mac App Store edition of IsiX also has a data collection declaration. Root and custom 404 pages bring the total to 54 HTML pages.

## Preview and maintain

From the repository root:

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Open http://127.0.0.1:8080/. Stop the server with Ctrl+C.

New project copy is maintained in `content/apps/*.json`. After editing it, regenerate and validate:

```sh
python3 tools/build_site.py
python3 tools/check_site.py
git diff --check
```

These commands use only the Python standard library. Generated HTML is committed, so GitHub Pages needs no build command. AutoComp's existing page bodies are kept in their HTML files; the generator updates only their shared navigation and footer.

Shared styles are in `assets/site.css`. The AutoComp icon is the existing Safari extension asset. Eleven additional projects use their existing product icons from the source checkouts. Initials are used for DICOM-Swift, MTK, the DICOM agent suite, dicom-go, and the separate macOS IsiX section. The dicom-go example bundle uses the standard Fyne logo, which is not used as a project logo here. No application screenshots or DICOM samples are published here.

## Routes

Each base below also has `support/` and `privacy/` subpages.

| Project | Base route |
| --- | --- |
| AutoComp | `/apps/autocomp/` |
| Turing Lab | `/apps/turing-lab/` |
| IsiX DICOM Viewer | `/apps/isis-dicom-viewer/` |
| IsiX DICOM Viewer for macOS, Mac App Store edition | `/apps/isis-dicom-viewer-macos/` |
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

The Horos-derived macOS Mac App Store edition has separate privacy and data collection pages at `/apps/isis-dicom-viewer-macos/privacy/` and `/apps/isis-dicom-viewer-macos/data-collection/`. Its copy is maintained in `content/apps/isis-dicom-viewer-macos.json`; `privacy_date` sets this policy's effective date without changing other projects. The existing Apple/Android IsiX policy remains at its original route.

Only approved public repositories are linked. The DICOM agent suite describes its three components but links only dicom-skill and dicom-viewer-mcp-app, as requested by the owner.

## Publication

The publishing source is the root of `main`. `.nojekyll` keeps delivery as plain static files. Pushing does not configure GitHub Pages. Pages settings and App Store Connect are outside this site's maintenance workflow.

See `docs/site-validation.md` for the local checks and their limits.
