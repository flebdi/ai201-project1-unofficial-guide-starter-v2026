import re

import gate

_STOPWORDS = {
    "a", "an", "and", "are", "at", "did", "do", "does", "for", "in",
    "is", "of", "on", "or", "that", "the", "this", "to", "which",
}

# Negation contractions expand before matching, so "doesn't count" (an
# expects phrase) still matches an answer that spells it out as "do not
# count" — a difference in surface form, not in what's actually being said.
_CONTRACTIONS = {
    "don't": "do not", "doesn't": "does not", "didn't": "did not",
    "isn't": "is not", "aren't": "are not", "wasn't": "was not",
    "weren't": "were not", "won't": "will not", "can't": "can not",
    "couldn't": "could not", "shouldn't": "should not",
    "wouldn't": "would not", "hasn't": "has not", "haven't": "have not",
    "hadn't": "had not",
}


def _expand_contractions(text: str) -> str:
    text = text.lower()
    for contraction, expanded in _CONTRACTIONS.items():
        text = text.replace(contraction, expanded)
    return text


def _keywords(text: str) -> list[str]:
    """Meaningful words in `text`, lowercase, filler words dropped."""
    words = re.findall(r"[a-z0-9']+", _expand_contractions(text))
    return [w for w in words if w not in _STOPWORDS]


def judge(question: str, expects: str, answer: str, results) -> bool:
    """
    True if every meaningful word in `expects` shows up somewhere in the
    answer, in any order.

    An exact-phrase check was too strict for this corpus: it failed
    correct answers that used the source's own words but not the exact
    wording written into questions.py — e.g. the source says "through the
    end of week six" but an expects phrase said "week six is the latest".
    Checking words as substrings rather than exact tokens also tolerates
    plural/singular mismatches that come up a lot here ("hour" vs.
    "hours", "credit" vs. "credits").

    Contractions are expanded on both sides first ("doesn't" and "do not"
    become the same thing), since that mismatch showed up for real: the
    source says "don't count" but a generated answer spelled it out as
    "do not count against your financial aid" — same fact, different
    surface form. This does NOT paper over a genuine vocabulary mismatch:
    if the answer never mentions the concept at all, no amount of
    normalization makes its keywords show up, and the question correctly
    still fails.
    """
    if not expects:
        return False
    if answer == gate.REFUSAL:
        return False

    answer_norm = _expand_contractions(answer or "")
    keywords = _keywords(expects)
    if not keywords:
        return False
    return all(word in answer_norm for word in keywords)
