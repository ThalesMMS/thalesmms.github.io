# Project source review

Reviewed November 2, 2026 against local source checkouts and the site's reachable Git history. The directory keeps its 17 project routes. Product implementations, embedded libraries, development snapshots and distribution editions can differ.

| Site project | Current scope and resulting correction |
| --- | --- |
| AutoComp for Safari | Current extension adds phrase libraries, optional browser models, review, assistant, dictation and semantic search. Native macOS, mobile, Flutter, Chrome and OnlyOffice implementations are identified separately. Privacy remains specific to Safari. |
| IsiX DICOM Viewer | Separate Apple mobile/companion and Android stacks. Added supported local segmentation and CT assistance, including model-download disclosure. The Windows application and distributed macOS application have separate implementations. |
| IsiX DICOM Viewer for macOS | Presentation distinguishes GitHub stable, 6.0 beta and Mac App Store builds. Current configuration declares macOS 15 and architecture-specific packages. Privacy and data collection remain restricted to the App Store edition. Updated the renamed public source URL. |
| dicom-slides | Existing import, Office persistence and privacy descriptions remain consistent with the inspected source snapshot. |
| DICOM-Swift | Public 3.1.0 manifest declares Swift 6.2, iOS/visionOS 26 and macOS 15. Added optional HL7, CDA, FHIR and clinical-mapping products and their network/data scope. Embedded copies can differ. |
| MTK | Public core/fixtures and development MTKUI products are distinguished. Public manifest still declares Apple OS 26 minimums. |
| DICOM tools for AI agents | Distinguished current composite Query/Retrieve viewer, coding-host HTML output and separate standalone prototype. Updated HTTP authentication guidance by implementation. |
| TotalSegmentator plugin | Linked Swift plugin pins TotalSegmentator 2.18.0 for managed setup. Distinguished the separate native reconstruction, IsiX plugin interfaces and application-native segmentation. Kept Python telemetry disclosure. |
| RadRef | Existing five reference areas and local storage descriptions remain consistent with the inspected implementation. |
| dicom-go | Added supported file-set, Storage Commitment and NIfTI workflows. Distinguished the library from its TwinViewer desktop consumer. |
| Podcast Intelligence | Desktop/server storage and provider boundaries remain explicit. Local desktop packaging does not make remote AI inference local. |
| CodeAtlas | Newer development builds have an optional Codex provider; the older snapshot can lack it. Settings, source transmission and CLI-owned authentication are described by build. |
| The Legend of Source | Added implemented Codex authentication, isolated credential storage, release-note generation and HTML export. Embeddings remain separately configured. |
| Scout | Corrected obsolete plaintext-only credential wording. Current code uses a native vault with verified migration and a visible plaintext fallback when unavailable. Codex logout protects externally owned authentication files. Word and OnlyOffice integrations are separate. |
| MacPGP | Distinguished the older linked snapshot from newer backup and credential changes. Encrypted backup support does not imply encryption of every local file. |
| Video Subtitler | Added iOS/iPadOS 18 minimum, SRT import and current file/Keychain protection. Distinguished the related desktop project and kept privacy specific to iOS. |
| Turing Lab | Retained implemented formal-system scope and explicit platform targets. Code availability, device qualification and store distribution remain separate. |

The detailed local report records source revisions, dirty working trees and remaining uncertainty. It is kept outside published content because it references private checkouts. Hashes identify future source drift; they do not automatically certify the text.

Separate implementations without their own policy on this site are identified as outside the listed policy's scope. This review did not qualify their distribution, store status or runtime behavior. See [site validation](site-validation.md) for checks actually run.
