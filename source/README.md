# Source data

Original exports and inventories. Nothing here is read by the coding
runners themselves -- only by the prep/preflight scripts noted below.
Prepared text the coding runners actually read lives under `data/`, not here.

```
source/
│
├── academic_records_328.csv
│     328-row list. record_id = Covidence #. doi_url where a DOI exists (245/328).
│     text_level says what was coded; the 231 full_text PDFs are in
│     academic_pdfs/ below.
│
│     328
│     ├── full_text        231   retrieved PDF; coded at title + abstract + full text
│     ├── title_abstract    89   no PDF; coded at title + abstract
│     └── title_only         8   no PDF, no abstract; coded at title only
│
│     Read by scripts/local_inputs.load_correspondence().
│
├── academic_corpus_328_covidence_export.csv
│     Covidence screening export for the same 328 IDs (column Covidence #).
│     Read only by scripts/prepare_academic_title_abstract.py, which writes
│     data/academic/title_abstract/ from it -- not by coding itself.
│
├── academic_pdfs/
│     The 231 full_text PDFs themselves (see academic_pdfs/README.md). Not
│     read by coding; data/academic/fulltext/ is extracted from these by
│     scripts/prepare_academic_fulltext.py, a separate prep step. Excluded
│     from Git.
│
└── nonacademic_documents_42.csv
      42-row list. webpage_url = page where the document was found.
      direct_file_url = standalone file URL if one exists separately from that page.
      download_url = filled for all 42 (file URL if separate; otherwise the webpage).

      42
      ├── Government            15
      ├── Professional body     18
      └── Media/news             9

      format
      ├── HTML page             23
      ├── Printed from webpage  11
      └── Native PDF             8

      duplicate is a retained inventory annotation only; runners ignore it.
      Read only by scripts/check_inputs.py, not by coding itself.
```

**Redacted abstracts.** Nonempty `Abstract` values in the public version of `academic_corpus_328_covidence_export.csv` have been replaced with `[REDACTED: third-party abstract]`. Bibliographic fields, including titles and identifiers, are retained. Redaction is a separate post-processing step solely for public release on GitHub, not part of terminology coding or analysis. It does not change the deposited codes or aggregate results. Unredacted inputs are retained locally and excluded from the public repository. Redacted placeholders must not be used to reproduce the analysis; supply the corresponding abstracts before preparing inputs and running coding.
