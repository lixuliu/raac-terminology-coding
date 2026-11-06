# Academic prepared text

What `scripts/run_objective1_academic_coding.py` actually reads, via
`scripts/local_inputs.py`. Built from `../../source/` (see
`../../source/README.md`); never edit these by hand.

```
data/academic/
│
├── fulltext/
│     One {record_id}.txt per full_text record (231). See fulltext/README.md.
│
└── title_abstract/
      One {record_id}.txt per record (328, all of them). Materialized by
      scripts/prepare_academic_title_abstract.py from
      source/academic_corpus_328_covidence_export.csv. See
      title_abstract/README.md.
```
