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

**3 (Unit 2).** I used Claude Code to run the Unit 2 test. It stopped me
before running anything: my working copy had all five test questions
swapped for harder ones after the originals had already scored 5/5, which
would have broken the "criteria existed before results" history. It asked
which set should be graded, and I chose to restore the Unit 1 questions and
keep the harder ones as a separately labelled stress set. It also wrote a
throwaway script to count criteria 1, 2 and 5 per run from the results
files, and that caught the pattern I hadn't seen: the add/drop answers
dropped their citation along with the answer, which made the criterion 2
miss and the wrong answer one cause, not two. I picked the grounding-prompt
fix from its suggestions because retrieval was already 5/5. I kept the
`expects` phrase it pointed out as unmatchable ("latest") unchanged instead
of editing it after seeing the answers.

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

Later check with the scorer: once `scorer.py` existed, a scored re-run of the
same five questions (`results/run_2026-09-23_2135.md`) came out pass on all
15 runs, agreeing with the hand judgement above.

### Stress set — Before

All five graded questions cleared every criterion on the first try, which
says more about the questions than the system. So I wrote five harder
questions (`STRESS_QUESTIONS` in `questions.py`) to see whether the 5/5 was
the system or just easy questions.

**Read this plainly:** these were written *after* the graded results
existed, so they are **not** the test my criteria are graded against. The
Unit 1 `QUESTIONS` are, and they're unchanged in the commit history.
The stress set is extra evidence, and it's where the improvement below got
its target. (I briefly swapped the stress questions into `QUESTIONS` itself
while trying them out. That swap was never committed, and I reverted it
into a separate list rather than quietly replacing the originals.)

`python run_eval.py --stress --label before_stress` →
`results/run_2026-09-30_0111_before_stress.md`. The same five criteria and
targets:

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 4/5 | 4/5 | 5/5 | **MISSED** |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks read as complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Named source is the correct source | 4 of 5 | 4/5 | 4/5 | 5/5 | MET |

Scorer (`scorer.py::judge`, answer contains the `expects` fact): the add/drop
question failed 3/3, the other four passed 3/3.

How the counts were made: criterion 1 means a document that holds the
answer is in `Sources retrieved`. Criterion 2 means the answer text names
any `.txt` file. Criterion 5 means every file the answer names is one that
holds the answer (a no-source answer counts as a fail). I counted these per
run with a small script rather than by eye, and checked the misses by
reading them.

**Real output, criterion 2 miss.** `generate.py::answer_from_chunks`, run 1,
"What happens if a student wants to add or drop a course after the
deadline?". Retrieved `admin_add_drop_deadline.txt` and
`admin_withdrawal_deadline.txt` among five:
```
Based on the provided documents, there is no information explaining what happens if a student tries to add or drop a course *after* the respective deadlines (which are the end of the second week for adding, and the end of week six for dropping). Therefore, I do not have enough information to answer this question.
```
No source named. Run 2 was the same; run 3 added
`(Source: admin_add_drop_deadline.txt)`.

**Near-miss probe (before).** These are in-topic questions whose fact isn't
in any document ("What professor teaches CS 210?", "How much does a meal
plan cost per semester?"). The gate lets them through (0.440, 0.484), so
only the prompt stops a made-up answer. Refused correctly 6/6
(`results/nearmiss_2026-09-30_before.md`), e.g.:
```
I don't have enough information to answer what professor teaches CS 210, as the provided documents do not mention any professors.
```

## Verdicts

The verdicts are against the **graded** questions and the Unit 1 targets.
The stress-set row is reported separately and doesn't replace them.

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer (4 of 5) | MET | 5/5 in all three runs. Retrieval is deterministic, so this is one result three times, and it clears 4 of 5 with room to spare. |
| 2 | Every answer names a source (5 of 5) | MET | 15 of 15 answers name a `.txt` file. Not close on the graded set. **On the stress set it was MISSED (4, 4, 5)**. A 5-of-5 target means one uncited answer in any run is a miss, and two runs had one. |
| 3 | Gate stops out-of-corpus questions (4 of 5) | MET | 5/5 refused in one deterministic pass. The closest out-of-corpus question (0.825) is still 0.225 over the 0.6 cutoff. |
| 4 | Chunks read as complete thoughts (4 of 5) | MET | All 5 sampled chunks are whole posts with no cut sentence. The sample (`app.py chunks -n 5`) is evenly spaced, not random, so it's the same 5 chunks every time: one measurement, not three. |
| 5 | Named source is the correct source (4 of 5) | MET | 15 of 15 graded answers name only files that hold the answer. On the stress set it was 4, 4, 5. Every run is still at least 4, so MET there too, but that's the closest call in this whole log. |

**Arguing the opposite.** The strongest case against "all MET" is that
criterion 5 and criterion 1 can both pass on an answer that's *wrong*.
Stress-set run 3 cites the correct file and then says the information isn't
there. My criteria never check whether the answer is right, only whether
the pieces around it are. That's a flaw in the criteria, not a reason to
change the verdicts, and it's in What I'd Do Differently.

No criterion was revised. `criteria.md` is unchanged from Unit 1.

## Diagnoses

**Graded set: no misses.** Honestly, that means the targets were set low,
not that the system is excellent. Every graded question has one short
document that states the answer in almost the question's own words
("Midterms are curved"), and every post is a single chunk. So criteria 1,
4 and 5 were close to guaranteed by the corpus's shape. The one I'd
tighten most is **criterion 4**. With 88 posts and 88 chunks it can't
really fail. I'd replace it with "for 4 of 5 questions whose answer spans
two documents, both documents are in the top 5". That's the case the
stress set shows is actually hard.

**Stress set: criterion 2 missed. Stage: generation.**

The add/drop question's answer is in retrieval twice over:
`admin_add_drop_deadline.txt` ("a drop after week two shows as a W on your
transcript") and `admin_withdrawal_deadline.txt` ("Dropping ends at week
six. Withdrawal runs to week ten, requires an adviser signature…") were
both retrieved on every run (best distance 0.292). So it's not loading,
chunking, embedding or retrieval. The model had both chunks in its prompt.

The mechanism is in `GROUNDING_INSTRUCTION` (`generate.py`). It gave the
model two options: answer, or "if the documents don't cover the question,
say you don't have enough information". The question as a student asks it
("what happens after the deadline") isn't answered by any *single* sentence.
You have to join "drop after week 2 → W" with "after week 6 it's a
withdrawal, to week 10". The prompt never said an answer can be assembled
from two documents, so the model picked "don't cover". Once it's in refusal
mode, the rule "name the document your answer came from" doesn't apply,
because there *is* no answer. So in 2 of 3 runs it cited nothing. **One
cause, two symptoms:** a wrong answer, and a criterion 2 miss.

**Pattern.** The only failure across 30 graded and stress runs is the only
question whose answer needs two documents combined. Every question with a
one-document answer passed every run.

**A measurement problem found along the way.** The add/drop `expects`
phrase ("week six is the latest") contains "latest", a word that appears in
no document in the corpus. `scorer.py` requires every keyword, so this
question can **never** pass the scorer, even with a perfect answer. The
scorer failures on this question are real (I read every answer and they
really are wrong). But the scorer alone can't tell a fixed answer from a
broken one here, so for the after-run I judged this question by reading
it.

## The Improvement

**What I changed:** `GROUNDING_INSTRUCTION` in `generate.py`, and nothing
else. Chunking, top-k, the gate and retrieval are untouched (commit
`9a8683d`). The prompt now says: an answer may be spread across documents,
so combine them. If the documents cover part of the question, answer that
part and say what's missing rather than refusing all of it. Refuse only if
nothing bears on the question. Name every document used, including for a
partial answer.

**Why I picked it:** the diagnosis put the failure in generation. Both
answer documents were retrieved, and the prompt's answer-or-refuse framing
turned them into an uncited refusal. So the fix belongs in the prompt, not
in retrieval. Hybrid search (BM25) would have been the wrong pick:
retrieval already finds the answer 5/5.

**The risk I measured for:** loosening "refuse if not covered" could make
the model invent answers to near-miss questions. So I re-ran the near-miss
probe too.

### Run Log — After

**Graded set:** `python run_eval.py --label after` →
`results/run_2026-09-30_0115_after.md`

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks read as complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Named source is the correct source | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

Real output, run 1, `generate.py::answer_from_chunks`:
```
Yes, the midterms are curved in CS 210 (though the final is not).

Sources used: `course_cs_210_exams.txt` and `course_cs_210.txt`.
```

**Stress set:** `python run_eval.py --stress --label after_stress`, run
**twice**: `results/run_2026-09-30_0117_after_stress.md` and
`results/run_2026-09-30_0118_after_stress.md`. A background run looked
stalled, so I started a second one, and both finished. Both are real,
independent passes, so both are reported. That makes six runs.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Run 6 | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | MET (was MISSED) |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks read as complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Named source is the correct source | 4 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | MET |

Add/drop answer, by reading it: **still wrong in 6/6**, but now *partly*
right in 5 of the 6 instead of 0 of 3. Real output, run 3 of the 0117 file:
```
Based on the provided documents:

* You can add a course through the end of the second week (admin_add_drop_deadline.txt). The documents do not state what happens if a student tries to add a course *after* this deadline.
* Dropping a course is allowed through the end of week six, though a drop after week two results in a "W" on your transcript (admin_add_drop_deadline.txt, admin_withdrawal_deadline.txt). The documents do not state what happens if a student tries to drop a course *after* the week six deadline.

Documents used: admin_add_drop_deadline.txt, admin_withdrawal_deadline.txt
```

**Near-miss probe (after):** still refused 6/6, with nothing invented
(`results/nearmiss_2026-09-30_after.md`). One refusal now also lists the
CS 210 files it checked, which is harmless.

| | Before | After |
|---|---|---|
| Graded set, all 5 criteria | 5/5 ×3 | 5/5 ×3 |
| Stress set, criterion 2 | 4, 4, 5 (MISSED) | 5 ×6 (MET) |
| Add/drop answer states the W-after-week-two fact | 0 of 3 | 5 of 6 |
| Add/drop answer mentions withdrawal to week ten | 0 of 3 | 0 of 6 |
| Near-miss correctly refused | 6 of 6 | 6 of 6 |

**Did it help?** Yes, on what it targeted, and I can say how I know.
Criterion 2 on the stress set went from missed (4, 4, 5) to met in all six
runs, and the near-miss refusals didn't regress. It **did not** fix the
answer itself. The model now gives the part it can find, but it still
never connects dropping to withdrawal. So the uncited refusal is gone,
and the wrong answer is only half-fixed.

## What's Still Broken

**The add/drop answer (stress set) is still incomplete in 6 of 6 runs.**
The model now answers partially, but it treats the withdrawal document as
unrelated. That's defensible from the text, which literally opens with
"Withdrawal is a different thing from dropping". But a student asking
"what if I'm past the drop deadline" needs exactly that document. The next
thing I'd try is still in generation: a few-shot example in the prompt
showing a "past deadline → here is the other route" answer. Or I'd check
whether the question is simply ambiguous, and rewrite it as "…after the
drop deadline in week six?", then see whether the model links the two.
I stopped here because the unit allows one change, and this one did what
it was aimed at (the missing citation). Stacking a second prompt tweak on
top would make the two impossible to tell apart.

**The scorer can't measure the add/drop question.** Its `expects` needs
"latest", which no document says. I left it alone, because rewriting an
`expects` after seeing the answers is exactly the "loosen it until it
passes" move this unit warns about. A fix should be written *before* the
next run, e.g. `expects: "withdraw"`, and it should be said out loud as a
change.

**Criterion 2 only checks that a source is named, not that it came from the
right place.** After the fix, one near-miss refusal lists three CS 210
files, which technically "names a source" on an answer that has none.

No criterion on the graded set is missed, so there's nothing there to fix.
The honest problem with the graded set is that it was too easy to tell me
much.

## What I'd Do Differently

- **Add an answer-correctness criterion.** None of my five checks whether
  the answer is *right*. They check retrieval, citation, the gate and
  chunking. A wrong answer that cites the correct file passes criteria 1,
  2 and 5 (stress-set run 3 before the fix did exactly that). I'd add: "For
  at least 4 of 5 questions, the answer states the fact in `expects`", with
  `expects` written from the source's own words so a correct answer *can*
  match it.
- **Replace criterion 4.** When every post fits in one chunk, "chunks read
  as complete thoughts" can't fail. It measured the corpus, not my chunker.
- **Write questions that need two documents.** Every graded question had a
  one-document, near-verbatim answer. The single real failure I found was
  the only question that needed two documents joined. At least two of the
  five should be like that.
- **Make criterion 5 say what happens when no source is named.** I had to
  decide that (it counts as a fail) while scoring, which means the
  criterion didn't fully define itself.
