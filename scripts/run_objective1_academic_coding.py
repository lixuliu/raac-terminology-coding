"""academic terminology coding. Calculation follows the uniform-rule analysis.
Only project-local input loading and output paths are adapted.
Optional validation and publication cleanup are separate scripts.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

from local_inputs import load_correspondence, load_screening_csv, load_academic_pages

HERE = Path(__file__).resolve().parent
RESULTS_DIR = HERE.parent / 'results' / 'academic'
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
from term_coding_core import PATTERNS, code_document


def run():
    correspondence = load_correspondence()
    screening = load_screening_csv()

    codes = []
    all_evidence = []
    for rid, row in correspondence.items():
        status = row[2]
        csv_row = screening[rid]
        title = csv_row['Title'] or ''
        abstract = csv_row['Abstract'] or ''

        texts = [('title', 0, title, 'screening_csv')]
        has_fulltext = status == 'PDF matched'
        if abstract.strip():
            texts.append(('abstract', 0, abstract, 'screening_csv'))

        if has_fulltext:
            src_path = Path(row[9].split('\n')[0].strip())
            pages = load_academic_pages(rid)
            for i, t in enumerate(pages):
                texts.append(('fulltext', i + 1, t, src_path.name))

        code, evidence = code_document(rid, texts)
        all_evidence.extend(evidence)

        out_row = {
            'record_id': rid,
            'title': title,
            'abstract_available': bool(abstract.strip()),
            'fulltext_coded': has_fulltext,
            'pdf_correspondence_status': status,
        }
        for scope in ('title', 'abstract', 'fulltext'):
            scope_has_text = (
                scope == 'title'
                or (scope == 'abstract' and bool(abstract.strip()))
                or (scope == 'fulltext' and has_fulltext)
            )
            for term in PATTERNS:
                key = f'{scope}_{term}'
                out_row[key] = code.get(key, 0) if scope_has_text else 'NA'
        out_row['metadata_RAAC_any'] = int(
            any(out_row[f'{s}_{t}'] == 1 for s in ('title', 'abstract') for t in ('RAAC_acronym', 'RAAC_full_phrase'))
        )
        codes.append(out_row)

    fieldnames = list(codes[0].keys())
    with (RESULTS_DIR / 'academic_lexical_codes_328.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(codes)

    ev_fieldnames = ['record_id', 'scope', 'term', 'page', 'match', 'context', 'source']
    with (RESULTS_DIR / 'academic_lexical_evidence.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=ev_fieldnames)
        w.writeheader()
        w.writerows(all_evidence)

    summary = {
        'n_records': len(codes),
        'n_fulltext_coded': sum(1 for r in codes if r['fulltext_coded']),
        'n_abstract_available': sum(1 for r in codes if r['abstract_available']),
        'n_title_only': sum(1 for r in codes if not r['abstract_available']),
    }
    for scope in ('title', 'abstract', 'fulltext'):
        for term in PATTERNS:
            key = f'{scope}_{term}'
            summary[key] = sum(1 for r in codes if r[key] == 1)
    summary['metadata_RAAC_any'] = sum(r['metadata_RAAC_any'] for r in codes)

    (RESULTS_DIR / 'academic_lexical_summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    run()
