# Academic source PDFs

The 231 original PDFs for the `full_text` academic records, self-contained
within this project (not a reference to any other project or folder).
Filenames are `{record_id}_{original_filename}.pdf`, e.g.
`#100_10.3390_ma14020390.pdf`.

`data/academic/fulltext/{record_id}.txt` is extracted from these PDFs --
that is the only link between the two. The extraction step is
`../../scripts/prepare_academic_fulltext.py` (see that script's docstring
for setup: it needs the third-party `pypdf` package, via a project-local
`.venv/`, unlike the coding runners which are standard-library-only).

The copy of `data/academic/fulltext/` currently checked into this project
was NOT produced by that script -- it predates it, from an earlier
extraction pass with a different (unrecorded) tool. Re-running
`prepare_academic_fulltext.py` will very likely change the extracted text
in small ways (line breaks, ligatures, a few garbled glyphs in subset
fonts) and therefore the coding results slightly, same as swapping any PDF
extraction tool for another. Only re-run it, and only re-run coding
afterwards, if you deliberately want to refresh `fulltext/` from this PDF
copy -- not as a routine step.

PDFs are excluded from Git (see `.gitignore`): this folder exists so the
project is self-contained locally, not so the PDFs get published.
