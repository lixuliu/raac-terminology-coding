"""One-time prep step: materialize one Title+Abstract .txt per record from
source/academic_corpus_328_covidence_export.csv into
data/academic/title_abstract/, in the same format fulltext/ uses for its own
per-record files. Running this is what keeps the Covidence export out of the
coding runner's reach -- local_inputs.load_screening_csv() reads
title_abstract/, not the export, so coding itself never touches that CSV.
Re-run after the export changes; idempotent otherwise."""
import csv
from local_inputs import SOURCE, ACADEMIC_DATA

def prepare():
    rows = list(csv.DictReader((SOURCE / 'academic_corpus_328_covidence_export.csv').open(encoding='utf-8-sig')))
    out_dir = ACADEMIC_DATA / 'title_abstract'
    out_dir.mkdir(parents=True, exist_ok=True)
    for r in rows:
        rid = r['Covidence #']
        content = (
            f"Covidence #: {rid}\nTitle: {r['Title']}\n"
            f"Authors: {r['Authors']}\nYear: {r['Published Year']}\n"
            f"Journal: {r['Journal']}\nDOI: {r['DOI']}\n\n"
            f"Abstract:\n{r['Abstract']}\n"
        )
        (out_dir / f'{rid}.txt').write_text(content, encoding='utf-8')
    assert len(rows) == 328, f'expected 328 rows, got {len(rows)}'
    print(f'Wrote {len(rows)} files to {out_dir}')

if __name__ == '__main__':
    prepare()
