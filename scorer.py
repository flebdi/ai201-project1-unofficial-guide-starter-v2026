import re

import gate

_STOPWORDS = {
    "a", "an", "and", "are", "at", "did", "do", "does", "for", "in",
    "is", "of", "on", "or", "that", "the", "this", "to", "which",
}


def _keywords(text: str) -> list[str]:
    """Meaningful words in `text`, lowercase, filler words dropped."""
    words = re.findall(r"[a-z0-9']+", text.lower())
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

    This does NOT paper over every mismatch — an expects word that uses
    different vocabulary entirely from the source ("doesn't" where the
    source says "don't") will still correctly fail, because the words
    genuinely differ. That's a wording problem in questions.py to fix
    there, not something a scorer should quietly work around.
    """
    if not expects:
        return False
    if answer == gate.REFUSAL:
        return False

    answer_lower = (answer or "").lower()
    keywords = _keywords(expects)
    if not keywords:
        return False
    return all(word in answer_lower for word in keywords)
