# HBC survey — v3.11, 13 November 2026

Canonical data: `anc/survey_snapshot.json`. The website embeds this snapshot; the PDF, BibTeX, CSV and workbook use the same records.

337 references: 103 IC publications, 147 channel/model publications and 87 other references. IC energy comparisons contain 38 TX, 38 RX and 49 combined TX+RX operating points. Counts describe publications, not unique chips.

## Release provenance and limits

This release recovers the curated 326-record snapshot from the saved HBC_Catalogue_Overleaf.zip (version 5), preserving the 12 exclusions and stable reference IDs. The October 26 automation reported 333 records (102 IC, 141 models, 90 other), but its saved HTML/workbook were unavailable. Its seven-record delta has **not** been reconciled. This release should not be described as a verified superset of that unavailable snapshot.

The refresh adds records 339–349 after DOI/title duplicate checks. Publisher-deposited Crossref metadata verifies the ten journal/conference citations. The NFE preprint is verified against arXiv and remains in Other Literature. Sources are included in each record. The body-resonance Communications Engineering paper's year is corrected to 2026 using the publisher's volume 5, article 1, rather than its DOI's 2025 suffix.

Searches covered HBC, body-coupled/body-channel communication, galvanic implant links, current IEEE/publisher results, and selected 2025 backfills across groups. Two broad Crossref queries were rate-limited; web searches and the two successful Crossref searches supplied additional coverage. This is a literature refresh, not an exhaustive re-audit of every inherited technical value.

The two added IC publications have no new energy comparison points. The ESSERC 2025 paper is the conference companion of record 003; its title's 0.7 pJ/bit front-end figure is not treated as full-receiver energy. The transdural telemetry article has fabricated TX/RX ASICs, but its duty-cycled board-level power has not been normalized to a comparable full-link measurement. Missing values remain blank.

Four inherited combined-energy points (158, 184, 186, 303) were withheld because their stored combined energy was less than a component energy at the same archived operating point. The original values and reasons remain in `withheldMetrics` in the canonical JSON. Source reconciliation is required before restoring them.

## Follow-up candidates

Four EMBC 2026 programme entries were found but are not counted as confirmed publications pending proceedings/DOI verification:

- Biophysical Circuit Modeling of Galvanic Implant-to-Wearable Electro-Quasistatic Human Body Communication as Inter-Device Capacitive Coupling: https://cmsworkshops.com/EMBC2026/view_paper.php?PaperNum=2599&SessionID=1160
- Enhancing Channel Capacity of Time Domain Body Communication for Body Area Network: https://cmsworkshops.com/EMBC2026/view_paper.php?PaperNum=1924&SessionID=1160
- Spring-Inspired Minimally Invasive Electrode Design for Deeper Implants Using Electro-Quasistatic Human Body Communication: https://cmsworkshops.com/EMBC2026/view_paper.php?PaperNum=2678&SessionID=1160
- Electro-Quasistatic Galvanic Human Body Communication vs Inductive Coupling: Experimental Analysis of Orientation Robustness in Implant-to-Wearable Links: https://cmsworkshops.com/EMBC2026/view_paper.php?PaperNum=4871&SessionID=1160

## Rebuild

Run `python anc/make_catalogue.py` and `python anc/make_figures.py` (matplotlib/numpy), then compile `main.tex` twice with pdfLaTeX. The Overleaf ZIP opens directly with main.tex as its main document. The page generator in `anc/build_page.py` reuses the repository's shared navigation/assets and updates HBC_Survey.html. The workbook generator uses the @oai/artifact-tool runtime; the exported XLSX does not need that runtime to open.

## Validation

- All 337 IDs are unique; all 335 stored DOI values are unique. Prior exclusions remain absent.
- All 337 reference labels occur in the 12-page PDF. PDF compilation, links and rendered pages checked.
- JavaScript syntax and DOM tests passed: 50-paper pagination, search, category filters, DOI links, scope selection, point details and CSV newline handling.
- Workbook formula error scan passed; native scatter charts reference only IC_Energy. All four sheet views rendered and inspected.
- Browser visual verification was unavailable: local Chromium launch was blocked by the environment. Desktop/mobile visual review remains required before publishing.

The branch updates only HBC_Survey.html and the survey/ directory. Merging or deploying is a separate step; this release has not changed the live Purdue website.
