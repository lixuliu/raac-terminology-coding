# Academic results

Same 328 records as `source/academic_records_328.csv`. `record_id` = Covidence #. 0 / 1 / NA at title, abstract, and full text. NA = that text level was not available.

The current output follows the original calculation schema: `pdf_correspondence_status` describes the input group. It is not named `text_level` in the output CSV.

```
results/academic/
│
├── academic_lexical_codes_328.csv
│     one row per record; seven labels × three text levels
│
│     328
│     ├── full_text        231   title + abstract + full text coded
│     ├── title_abstract    89   title + abstract coded; full-text columns = NA
│     └── title_only         8   title coded; abstract and full-text columns = NA
│
├── academic_lexical_evidence.csv
│     one row per match (term, scope, page, context)
│
└── academic_lexical_summary.json
      aggregate counts

seven labels
├── RAAC_acronym
├── RAAC_full_phrase
├── reinforced_AAC
├── AAC_acronym
├── AAC_full_phrase
├── ALC_acronym
└── ALC_full_phrase
```

Re-running the coding script regenerates unredacted evidence. Apply this separate redaction step again before public release; the coding script itself is unchanged.

**Redacted evidence file.** Original-text excerpts in the `context` column of the public version of `academic_lexical_evidence.csv` have been replaced with `[REDACTED: third-party text]` to avoid redistributing third-party copyrighted text without confirmed permission. This redaction is a separate post-processing step performed solely to prepare the file for public release on GitHub. It is not part of the terminology-coding or analytical procedure implemented in this project and does not alter the matching procedure, record-level codes, match counts or aggregate results. The unredacted evidence file is retained locally and is not included in the public repository.
