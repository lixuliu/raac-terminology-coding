"""Prep step: extract per-page text from source/academic_pdfs/*.pdf into
data/academic/fulltext/{record_id}.txt, in the same \\n\\x0c\\n page-separator
format the coding runner already expects (local_inputs.load_academic_pages).

This is the PDF -> fulltext link for this project's own copy of the 231
source PDFs (source/academic_pdfs/, self-contained within this project --
see source/academic_pdfs/README.md). It is a prep step, not part of
coding: re-run it only if source/academic_pdfs/ changes, and re-run
scripts/run_objective1_academic_coding.py afterwards.

Needs the third-party `pypdf` package (not standard library, unlike the
coding runners). Set up once with:
    python3 -m venv .venv && .venv/bin/pip install pypdf
Then run with:
    .venv/bin/python3 scripts/prepare_academic_fulltext.py

Different pypdf versions, or a different PDF library entirely, can extract
slightly different text (line breaks, ligatures, column order) from the
same PDF -- this is a known, documented limitation of PDF text extraction
in general, not specific to this script.
"""
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit(
        'pypdf is not installed. Set up a venv and install it:\n'
        '    python3 -m venv .venv && .venv/bin/pip install pypdf\n'
        'then re-run with .venv/bin/python3, not the system python3.'
    )

from local_inputs import SOURCE, ACADEMIC_DATA

PDF_DIR = SOURCE / 'academic_pdfs'


def prepare():
    out_dir = ACADEMIC_DATA / 'fulltext'
    out_dir.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(PDF_DIR.glob('*.pdf'))
    assert pdfs, f'no PDFs found in {PDF_DIR}'
    n = 0
    for pdf_path in pdfs:
        record_id = pdf_path.name.split('_', 1)[0]
        reader = PdfReader(pdf_path)
        pages = [page.extract_text() or '' for page in reader.pages]
        (out_dir / f'{record_id}.txt').write_text('\n\x0c\n'.join(pages), encoding='utf-8')
        n += 1
    print(f'Extracted {n} PDFs from {PDF_DIR} into {out_dir}')


if __name__ == '__main__':
    prepare()
