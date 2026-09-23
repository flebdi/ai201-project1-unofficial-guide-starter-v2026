"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _sentences(paragraph: str) -> list[str]:
    return [s.strip() for s in _SENTENCE_SPLIT.split(paragraph.strip()) if s.strip()]


def _units(text: str, limit: int) -> list[str]:
    """
    Break a document into pieces short enough to pack without ever cutting a
    sentence in half.

    Paragraphs are the natural unit for campus_life posts — each one already
    holds a complete thought. A paragraph is only broken further, into
    sentences, if it alone is longer than `limit`, which never happens in
    this corpus but keeps the function honest on anything longer.
    """
    units: list[str] = []
    for paragraph in re.split(r"\n{2,}", text.strip()):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if len(paragraph) <= limit:
            units.append(paragraph)
        else:
            units.extend(_sentences(paragraph))
    return units


def _pack(units: list[str], limit: int, overlap: int) -> list[str]:
    """
    Greedily join units into pieces up to `limit` characters, repeating the
    trailing units of one piece at the start of the next so a chunk boundary
    never falls mid-sentence and never drops the sentence right before it.
    """

    def length(pieces: list[str]) -> int:
        return sum(len(p) for p in pieces) + max(len(pieces) - 1, 0)

    pieces: list[str] = []
    current: list[str] = []

    for unit in units:
        if current and length(current + [unit]) > limit:
            pieces.append("\n\n".join(current))
            carry: list[str] = []
            for prior in reversed(current):
                carry.insert(0, prior)
                if length(carry) >= overlap:
                    break
            current = carry
        current.append(unit)

    if current:
        pieces.append("\n\n".join(current))

    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents on paragraph and sentence boundaries, not a fixed
    character window.

    campus_life posts are short and single-topic — the longest is 549
    characters, well inside CHUNK_SIZE (600) — so almost every post survives
    as exactly one chunk, its paragraphs rejoined unchanged. The paragraph/
    sentence packing in `_units`/`_pack` only starts doing real work on a
    post that runs long enough to need it, and even then never cuts a
    sentence in half.

    One thing plain character windows get wrong on this corpus: a post's
    topic (which dining hall, which building, which course) usually lives
    only in its title line. A window that started partway through the body
    would lose it. So every piece after the first gets that title line
    carried back in.
    """
    limit = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP

    chunks: list[Chunk] = []
    for doc in documents:
        title = doc.text.split("\n", 1)[0].strip()
        pieces = _pack(_units(doc.text, limit), limit, overlap)

        for i, piece in enumerate(pieces):
            text = piece if title in piece else f"{title}\n\n{piece}"
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=i,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
