"""nonacademic terminology coding. Calculation follows the uniform-rule analysis.
Only project-local input loading and output paths are adapted.
Optional validation and publication cleanup are separate scripts.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS_DIR = HERE.parent / 'results' / 'nonacademic'
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
CORPUS_DIR = HERE.parent / 'data' / 'nonacademic' / 'fulltext'
from term_coding_core import PATTERNS, code_document


def strip_header(text):
    marker = '=' * 60
    idx = text.find(marker)
    if idx == -1:
        return text
    return text[idx + len(marker):].lstrip('\n')


def run():
    codes = []
    all_evidence = []
    for txt_path in sorted(CORPUS_DIR.rglob('*.txt')):
        category = txt_path.parent.name
        record_id = f'{category}/{txt_path.name}'
        raw = txt_path.read_text(encoding='utf-8')  # prepared inputs already exclude inventory headers
        texts = [('fulltext', 1, raw, record_id)]
        code, evidence = code_document(record_id, texts)
        all_evidence.extend(evidence)

        row = {'record_id': record_id, 'category': category}
        for term in PATTERNS:
            row[term] = code.get(f'fulltext_{term}', 0)
        row['any_RAAC'] = int(bool(row['RAAC_acronym'] or row['RAAC_full_phrase']))
        row['no_label_matched'] = int(not any(row[t] for t in PATTERNS))
        codes.append(row)

    assert len(codes) == 42, f'expected 42 documents, got {len(codes)}'

    fieldnames = list(codes[0].keys())
    with (RESULTS_DIR / 'nonacademic_lexical_codes_42.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(codes)

    ev_fieldnames = ['record_id', 'scope', 'term', 'page', 'match', 'context', 'source']
    with (RESULTS_DIR / 'nonacademic_lexical_evidence.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=ev_fieldnames)
        w.writeheader()
        w.writerows(all_evidence)

    def summarize(rows):
        n = len(rows)
        s = {'n_documents': n}
        for term in PATTERNS:
            s[term] = sum(r[term] for r in rows)
        s['any_RAAC'] = sum(r['any_RAAC'] for r in rows)
        s['no_label_matched'] = sum(r['no_label_matched'] for r in rows)
        by_cat = {}
        for cat in sorted(set(r['category'] for r in rows)):
            cat_rows = [r for r in rows if r['category'] == cat]
            cs = {'n': len(cat_rows)}
            for term in PATTERNS:
                cs[term] = sum(r[term] for r in cat_rows)
            cs['any_RAAC'] = sum(r['any_RAAC'] for r in cat_rows)
            cs['no_label_matched'] = sum(r['no_label_matched'] for r in cat_rows)
            by_cat[cat] = cs
        s['by_category'] = by_cat
        return s

    summary = {
        'as_collected_n42': summarize(codes),
        'note': 'All 42 input files are coded and included in aggregation. No deduplication is applied.',
    }
    (RESULTS_DIR / 'nonacademic_lexical_summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    run()
