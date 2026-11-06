"""Optional preflight only. Does not run coding or modify files."""
import csv
from pathlib import Path
from local_inputs import ROOT, SOURCE, ACADEMIC_DATA

def check():
    records = list(csv.DictReader((SOURCE / 'academic_records_328.csv').open(encoding='utf-8-sig')))
    required = [ACADEMIC_DATA / 'fulltext' / f"{r['record_id']}.txt" for r in records if r['text_level'] == 'full_text']
    docs = list(csv.DictReader((SOURCE / 'nonacademic_documents_42.csv').open(encoding='utf-8-sig')))
    categories = {'Government': 'government', 'Professional body': 'professional', 'Media/news': 'media and news'}
    NONACADEMIC_FULLTEXT = ROOT / 'data' / 'nonacademic' / 'fulltext'
    expected = {NONACADEMIC_FULLTEXT / categories[d['category']] / (Path(d['document']).stem + '.txt') for d in docs}
    required += sorted(expected)
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    extra = set(NONACADEMIC_FULLTEXT.rglob('*.txt')) - expected
    if missing or extra:
        raise RuntimeError(f'Missing inputs: {missing}; unexpected non-academic inputs: {sorted(map(str, extra))}')
    print('Inputs present: 231 academic texts and 42 non-academic texts. No files changed.')

if __name__ == '__main__':
    check()
