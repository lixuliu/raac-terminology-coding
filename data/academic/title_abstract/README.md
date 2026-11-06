# Academic title/abstract text

328 UTF-8 files named `{record_id}.txt` (e.g. `#1.txt`), one per academic
record -- all 328, not just the 231 full-text ones. Format:

```
Covidence #: #1
Title: ...
Authors: ...
Year: ...
Journal: ...
DOI: ...

Abstract:
...
```

Materialized by `../../../scripts/prepare_academic_title_abstract.py` from
`../../../source/academic_corpus_328_covidence_export.csv`. Re-run that
script after the export changes, before re-running coding.

**Redacted abstracts.** Nonempty abstracts in these public text files have been replaced with `[REDACTED: third-party abstract]`; titles and other bibliographic fields are unchanged. This is a separate post-processing step solely for GitHub publication, not a coding or analytical step. The unredacted prepared inputs are retained locally and excluded from Git. These public files document input structure but cannot reproduce the deposited results without the corresponding abstracts. Restore or independently supply unredacted inputs before running the coding scripts. No calculation code or deposited results were changed by redaction.
