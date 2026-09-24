# The Unofficial Guide

**flebdi** — corpus: `campus_life`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

The Unofficial Guide answers questions about `campus_life`, a corpus of 88
short student posts covering dining halls, dorms, courses, and the
administrative rules nobody explains properly. Ask it something specific —
"How long is the wait at Kestrel Commons during lunch?" or "Are the
midterms curved in CS 210?" — and it retrieves the posts that actually
answer it, names the source file, and refuses instead of guessing when
nothing in the corpus is close enough to the question. It's a command-line
tool: `python app.py ask "your question"`.

## Chunking Strategy

**Chunk size:** 600 characters
**Overlap:** 80 characters

`campus_life` posts are short and single-topic: 88 documents, 317 characters
on average, longest 549. Almost every post is one title line plus one to
three short paragraphs that answer one question, and reads as one complete
thought — so the right default is "one post stays one chunk," not a fixed
character window that happens to land in the middle of a paragraph.

The starter's 800-character window technically achieves that (nothing here
reaches 800 chars either), but only by accident — it would do the same thing
on a corpus where posts really did need splitting. I replaced it with a
chunker that decides on purpose: it packs whole paragraphs together up to
600 characters (comfortably above the 549-char longest post, but tight
enough that an unusually long post would actually get split rather than
disappear into an oversized window), falling back to sentence boundaries if
a single paragraph alone is ever too long, and never cutting a sentence in
half either way. 80 characters of overlap (roughly one sentence) carries the
trailing sentence of one piece into the next if a split ever happens, so the
following piece doesn't start without context.

One thing I noticed reading the docs that a plain window would have missed:
a post's topic — which dining hall, which building, which course — usually
lives only in its title line (e.g. `dining_pellew_dining_hall_followup.txt`
never repeats "Pellew" in its body text). Any chunk after the first piece of
a document gets that title line carried back in, so a chunk about "Hours are
7am–9pm" doesn't lose which dining hall it's talking about.

I didn't change my mind partway through — the corpus's shape (short,
self-contained posts) made "keep the post whole, split only if it's
genuinely too long" clear before I wrote any code.

Function: `chunker.py::split_documents`. `chunker.py::fallback_split` is kept
as the original, unchanged, for comparison.

## Sample Chunks

`python app.py chunks -n 5` output, spread across the corpus:

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

Each of these five reads as a complete thought on its own — no sentence cut
off at either end, and each names its own topic (course code, building name,
or dining hall) without needing a neighboring chunk or its filename.

## Sample Answer

**Question:** How long is the wait at Kestrel Commons during lunch?

**Answer:**

```
Based on the provided documents, the wait time at Kestrel Commons is 20 to
25 minutes between 12:15 and 1:00, and under 5 minutes before 11:45.

Source: dining_kestrel_commons.txt (and dining_kestrel_commons_followup.txt)
```

(Best distance 0.167, cutoff 0.6 — well inside the gate.)

**My relevance cutoff:** 0.6 (the starter's default — I measured against it
rather than changing it, since it already sits in the gap).

I ran my 5 test questions and the 5 `OUT_OF_SCOPE` questions through
`python app.py retrieve "..."` and recorded the best (top-1) distance for
each. The two groups don't overlap at all — the worst in-corpus question
(0.429) is still almost 0.4 below the best out-of-corpus question (0.825) —
so 0.6 sits comfortably in the middle of a wide gap, not close to either
edge.

| Question | In corpus? | Best distance |
|---|---|---|
| How long is the wait at Kestrel Commons during lunch? | yes | 0.167 |
| Is there an enforced quiet time in Morrow House? | yes | 0.295 |
| Can you study during your shift at an on-campus dining job? | yes | 0.265 |
| How often does the campus shuttle run on weekdays? | yes | 0.425 |
| Are the midterms curved in CS 210? | yes | 0.429 |
| What is the capital of Mongolia? | no | 0.825 |
| How do I change the oil in a diesel engine? | no | 0.934 |
| Who won the 1994 World Cup? | no | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.844 |
| How do I write a for loop in Rust? | no | 0.896 |

I also checked the grounding instruction (`GROUNDING_INSTRUCTION` in
`generate.py`) against a near-miss case: a question that's topically
in-corpus (so it passes the gate) but whose specific fact isn't actually in
any document. Asking "What professor teaches CS 210?" retrieved the CS 210
docs at distance 0.440 (under the 0.6 cutoff, so the gate let it through),
and the model correctly answered "I don't have enough information... the
provided documents do not mention the professor's name" instead of
inventing one. That held without needing to tighten the instruction further.

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I asked Claude to just write criteria #4 and #5 in `criteria.md`
directly. It refused, pointing at the assignment's own instruction ("don't
ask an AI to write your criteria... a criterion you didn't write is one you
can't defend") and offered a guided-extraction alternative instead: it asked
me multiple-choice questions about what "wrong-sized" would actually mean
for my chunks, what fraction should count as passing, and what I wanted
criterion #5 to hold the system accountable for. I picked the options
(cuts off mid-sentence, 4 of 5, correct-source-not-just-present, 4 of 5), and
the final sentences were assembled from those picks rather than written
wholesale by the model. I did later tell it to draft the 5 test questions in
`questions.py` outright, since that file didn't carry the same explicit
warning — so the two files ended up written two different ways.

**2.** I asked Claude to design and write the new chunker
(`chunker.py::split_documents`) for Milestone 3. It came back with a
paragraph/sentence-aware packer — 600-character chunk size, 80-character
overlap, titles carried into any continuation piece — justified against the
corpus's actual stats (88 docs, 317 characters average, 549 longest) rather
than a round number. Rather than accepting the code as correct on sight, I
had it re-run `python app.py index` and `python app.py chunks -n 5` so I
could check the claimed output (88 chunks, same length stats, five sample
chunks that each read as a complete thought) against what the code actually
produced before it went in the README.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks read as complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Named source is the correct source | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

No `scorer.py` exists yet, so I judged each of the 15 runs by hand against
`results/run_2026-09-23_2032_before.md`. Criteria 1, 3, and 4 depend only on
retrieval and chunking, which are deterministic — `store.py::search` and
`chunker.py::split_documents` gave the identical sources/chunks on every run,
so those rows are the same number three times over, same as the example.
Criteria 2 and 5 depend on what the model actually wrote
(`generate.py::answer_from_chunks`), which did vary in phrasing between runs
— but not in substance, so they still landed at 5/5 every time.

Real output, one example per criterion, from the `before` run:

**Criterion 1** (retrieved chunk contains the answer) — `store.py::search`
for "Are the midterms curved in CS 210?" retrieved `course_cs_210_exams.txt`,
whose text is:
```
CS 210 Data Structures — assessment

Two midterms and a final, all drawn from lecture material rather than the
textbook. Midterms are curved, the final is not.

Do the labs even though they're only 10% — the exams reuse the lab problems.
```
which contains the answer ("Midterms are curved").

**Criterion 2** (every answer names a source) — `generate.py::answer_from_chunks`,
run 1, for "How long is the wait at Kestrel Commons during lunch?":
```
The wait time at Kestrel Commons is 20 to 25 minutes between 12:15 and 1:00,
and under 5 minutes before 11:45.

Source: `dining_kestrel_commons.txt` (and similar information in
`dining_kestrel_commons_followup.txt`).
```

**Criterion 3** (gate stops out-of-corpus questions) — `run_eval.py::check_out_of_scope`
+ `gate.py::check`:
```
refused  (best distance 0.825)  What is the capital of Mongolia?
refused  (best distance 0.934)  How do I change the oil in a diesel engine?
refused  (best distance 0.886)  Who won the 1994 World Cup?
refused  (best distance 0.844)  What is the recommended dosage of ibuprofen for a headache?
refused  (best distance 0.896)  How do I write a for loop in Rust?
-> gate refused 5 of 5
```

**Criterion 4** (chunks read as complete thoughts) — `chunker.py::split_documents`,
one of the 5 sampled chunks (also in Sample Chunks above):
```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no
problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because
you're learning the format.
```
A complete thought start to finish, no sentence cut off at either end.

**Criterion 5** (named source is the correct source) — the same run 1 CS 210
answer as above: it cites `course_cs_210_exams.txt` and `course_cs_210.txt`,
and `course_cs_210_exams.txt` is the document that actually states "Midterms
are curved" — not just any retrieved file (the other 4 retrieved sources
that run were other courses' exam pages, correctly left out of the citation).

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
