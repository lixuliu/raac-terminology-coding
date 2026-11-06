"""Shared regex matching for the 7 terminology labels (RAAC/AAC/ALC, acronym
and full phrase, plus "reinforced AAC"), imported by both corpus runners in
this folder so the two sides stay comparable.
"""
import re
import unicodedata

PATTERNS = {
    'RAAC_acronym': r'(?<!\w)raac(?!\w)',
    'RAAC_full_phrase': r'(?<!\w)reinforced[\s\-]+autoclaved[\s\-]+aerated[\s\-]+concrete(?!\w)',
    'reinforced_AAC': r'(?<!\w)reinforced[\s\-]+aac(?!\w)',
    'AAC_acronym': r'(?<!\w)aac(?!\w)',
    'AAC_full_phrase': r'(?<!\w)autoclaved[\s\-]+aerated[\s\-]+concrete(?!\w)',
    'ALC_acronym': r'(?<!\w)alc(?!\w)',
    'ALC_full_phrase': r'(?<!\w)autoclaved[\s\-]+lightweight[\s\-]+concrete(?!\w)',
}
COMPILED = {k: re.compile(v, re.I) for k, v in PATTERNS.items()}

REFERENCES_HEADING = re.compile(
    r'(?im)^\s*(?:\d+[. ]+)?(?:references|bibliography|literature cited)\s*[:\n]'
)


def clean_block(text):
    """Normalize a single block of text before matching. Identical for both corpora."""
    text = unicodedata.normalize('NFKC', text).replace('­', '')
    text = re.sub(r'(?<=[a-zA-Z])-\s*\n\s*(?=[a-zA-Z])', '', text)
    return text


def truncate_references_by_fraction(text, min_fraction=0.5):
    """Cut text at a references/bibliography heading if that heading starts at or
    past `min_fraction` of the way through the text. Generalizes the page-index
    check in the original academic script (i >= len(pages)/2) to a single block
    of text using character position instead of page index."""
    m = REFERENCES_HEADING.search(text)
    if m and m.start() >= len(text) * min_fraction:
        return text[:m.start()], True
    return text, False


def strip_known_boilerplate(text):
    """Strip repository/landing-page boilerplate that is not part of the document's
    own content. Harmless no-op if the strings are absent."""
    if 'See discussions, stats, and author profiles' in text[:200]:
        return ''
    if 'You may also like' in text:
        text = text.split('You may also like')[0]
    return text


def code_block(record_id, scope, page, text, source, manual_exclude=None):
    """Scan one (scope, page) block of text for all 7 terms.

    manual_exclude(record_id, term, scope, page, match, text) -> bool
        Optional callable for documented, record-specific false-positive
        exclusions (e.g. an equation variable, not a blanket rule).

    Returns (found: dict[term] -> list[context_str], evidence: list[dict]).
    """
    found = {t: [] for t in PATTERNS}
    evidence = []
    for term, pat in COMPILED.items():
        for m in pat.finditer(text):
            if term in ('RAAC_full_phrase', 'reinforced_AAC') and re.search(
                r'\bnon[\s\-]*$', text[max(0, m.start() - 12):m.start()], re.I
            ):
                continue
            if manual_exclude and manual_exclude(record_id, term, scope, page, m, text):
                continue
            context = ' '.join(text[max(0, m.start() - 150):m.end() + 190].split())
            found[term].append(context)
            evidence.append({
                'record_id': record_id, 'scope': scope, 'term': term, 'page': page,
                'match': m.group(), 'context': context, 'source': source,
            })
    return found, evidence


def code_document(record_id, texts, manual_exclude=None, truncate_fulltext_references=True):
    """texts: list of (scope, page, raw_text, source) for one document.
    scope is one of 'title', 'abstract', 'fulltext'.

    Returns (code: dict['{scope}_{term}'] -> 0/1, evidence: list[dict]).
    A scope present in `texts` is coded 0/1 for every term even if no block for
    that scope contains a match; a scope entirely absent from `texts` is left
    out of `code` by the caller (NA), not coded 0 here.
    """
    code = {}
    all_evidence = []
    by_scope = {}
    for scope, page, raw, source in texts:
        by_scope.setdefault(scope, []).append((page, raw, source))

    for scope, blocks in by_scope.items():
        scope_found = {t: [] for t in PATTERNS}
        for page, raw, source in blocks:
            text = clean_block(raw)
            text = strip_known_boilerplate(text)
            if not text:
                continue
            if scope == 'fulltext' and truncate_fulltext_references:
                text, _ = truncate_references_by_fraction(text)
            found, evidence = code_block(record_id, scope, page, text, source, manual_exclude)
            all_evidence.extend(evidence)
            for term in PATTERNS:
                scope_found[term].extend(found[term])
        for term in PATTERNS:
            code[f'{scope}_{term}'] = int(bool(scope_found[term]))

    return code, all_evidence
