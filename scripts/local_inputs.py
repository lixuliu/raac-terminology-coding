"""Project-local input adapter; no terminology matching or output cleanup."""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'source'
ACADEMIC_DATA = ROOT / 'data' / 'academic'
STATUS = {
    'full_text': 'PDF matched',
    'title_abstract': 'no PDF matched; abstract available',
    'title_only': 'no PDF matched; no abstract available',
}
TITLE_RE = re.compile(r'^Title: (.*)$', re.MULTILINE)

def load_correspondence():
    records = list(csv.DictReader((SOURCE / 'academic_records_328.csv').open(encoding='utf-8-sig')))
    rows = {}
    for rec in records:
        row = [None] * 10
        row[0] = rec['record_id']
        row[2] = STATUS[rec['text_level']]
        row[9] = str(ACADEMIC_DATA / 'fulltext' / f"{rec['record_id']}.txt")
        rows[row[0]] = row
    assert len(rows) == 328
    return rows

def load_screening_csv():
    """record_id -> {'Title', 'Abstract'}, from the per-record .txt files in
    data/academic/title_abstract/ (written by prepare_academic_title_abstract.py
    from source/academic_corpus_328_covidence_export.csv) -- not from that
    export CSV directly, so coding itself never touches it."""
    by_id = {}
    for p in (ACADEMIC_DATA / 'title_abstract').glob('*.txt'):
        text = p.read_text(encoding='utf-8')
        m = TITLE_RE.search(text)
        idx = text.find('Abstract:')
        abstract = text[idx + len('Abstract:'):].strip() if idx != -1 else ''
        by_id[p.stem] = {'Title': m.group(1).strip() if m else '', 'Abstract': abstract}
    assert len(by_id) == 328
    return by_id

def load_academic_pages(record_id):
    return (ACADEMIC_DATA / 'fulltext' / f'{record_id}.txt').read_text(encoding='utf-8').split('\n\x0c\n')
