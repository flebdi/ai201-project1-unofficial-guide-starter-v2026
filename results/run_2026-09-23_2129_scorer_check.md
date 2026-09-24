# Run log — scorer_check

- Produced by: `run_eval.py::main`
- Retrieval: `store.py::search`, chunks from `chunker.py::split_documents`
- Corpus: `campus_life` (index variant `default`)
- top-k: 5 · relevance cutoff: 0.6
- Runs per question: 3, caching off
- When: 2026-09-23 21:29

This table is one row per QUESTION. The run log your README asks for is
one row per CRITERION, so aggregate these into it — criterion 1 is how many
of your questions had the answer in the retrieved chunks, and so on.

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| How long is the wait at Kestrel Commons during lunch? | pass | pass | pass |
| Is there an enforced quiet time in Morrow House? | pass | pass | pass |
| Can you study during your shift at an on-campus dining job? | pass | pass | pass |
| How often does the campus shuttle run on weekdays? | pass | pass | pass |
| Are the midterms curved in CS 210? | pass | pass | pass |

---

## The relevance gate on out-of-corpus questions

Produced by `run_eval.py::check_out_of_scope`, cutoff 0.6. Refused 5 of 5.

Retrieval is deterministic and the gate is a comparison against a
fixed number, so these do not vary between runs — one pass over the
list is the whole measurement.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.934 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| How do I write a for loop in Rust? | 0.896 | refused |

---

## Real output

This is what the system actually produced. Paste the relevant parts
into your README underneath the table — the rubric asks for real
output as text, not a description of it.

### How long is the wait at Kestrel Commons during lunch? — run 1

- Best distance: 0.1674 (passed the gate)
- Sources retrieved: dining_halden_hall_followup.txt, dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt, dining_pellew_dining_hall_followup.txt, dining_the_ridgeway_cafe_followup.txt

```
Based on the provided documents, the wait time at Kestrel Commons is 20 to 25 minutes between 12:15 and 1:00, and under 5 minutes before 11:45. 

Source: `dining_kestrel_commons.txt` (and corroborated by `dining_kestrel_commons_followup.txt`).
```

### How long is the wait at Kestrel Commons during lunch? — run 2

- Best distance: 0.1674 (passed the gate)
- Sources retrieved: dining_halden_hall_followup.txt, dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt, dining_pellew_dining_hall_followup.txt, dining_the_ridgeway_cafe_followup.txt

```
Based on the provided documents, the wait time at Kestrel Commons is 20 to 25 minutes between 12:15 and 1:00, and under 5 minutes before 11:45. 

Source: `dining_kestrel_commons.txt` (and corroborated in `dining_kestrel_commons_followup.txt`).
```

### How long is the wait at Kestrel Commons during lunch? — run 3

- Best distance: 0.1674 (passed the gate)
- Sources retrieved: dining_halden_hall_followup.txt, dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt, dining_pellew_dining_hall_followup.txt, dining_the_ridgeway_cafe_followup.txt

```
At Kestrel Commons, the wait time is 20 to 25 minutes between 12:15 and 1:00, and under 5 minutes before 11:45. 

Source: `dining_kestrel_commons.txt` (and `dining_kestrel_commons_followup.txt`)
```

### Is there an enforced quiet time in Morrow House? — run 1

- Best distance: 0.2949 (passed the gate)
- Sources retrieved: housing_aldridge_hall_noise.txt, housing_calder_annexe_noise.txt, housing_morrow_house.txt, housing_morrow_house_noise.txt, study_library_hours.txt

```
No, there are no enforced quiet hours in Morrow House (Source: `housing_morrow_house.txt` and `housing_morrow_house_noise.txt`).
```

### Is there an enforced quiet time in Morrow House? — run 2

- Best distance: 0.2949 (passed the gate)
- Sources retrieved: housing_aldridge_hall_noise.txt, housing_calder_annexe_noise.txt, housing_morrow_house.txt, housing_morrow_house_noise.txt, study_library_hours.txt

```
No, there are no enforced quiet hours in Morrow House (housing_morrow_house.txt, housing_morrow_house_noise.txt).
```

### Is there an enforced quiet time in Morrow House? — run 3

- Best distance: 0.2949 (passed the gate)
- Sources retrieved: housing_aldridge_hall_noise.txt, housing_calder_annexe_noise.txt, housing_morrow_house.txt, housing_morrow_house_noise.txt, study_library_hours.txt

```
No, there are no enforced quiet hours in Morrow House (housing_morrow_house.txt and housing_morrow_house_noise.txt).
```

### Can you study during your shift at an on-campus dining job? — run 1

- Best distance: 0.2647 (passed the gate)
- Sources retrieved: admin_campus_jobs_and_financial_aid.txt, admin_meal_plan_changes.txt, dining_pellew_dining_hall_followup.txt, dining_verrill_street_grill.txt, money_jobs.txt

```
No, you cannot study during your shift at a dining job. (Source: money_jobs.txt)
```

### Can you study during your shift at an on-campus dining job? — run 2

- Best distance: 0.2647 (passed the gate)
- Sources retrieved: admin_campus_jobs_and_financial_aid.txt, admin_meal_plan_changes.txt, dining_pellew_dining_hall_followup.txt, dining_verrill_street_grill.txt, money_jobs.txt

```
No, you cannot study during your shift at an on-campus dining job. 

Source: money_jobs.txt
```

### Can you study during your shift at an on-campus dining job? — run 3

- Best distance: 0.2647 (passed the gate)
- Sources retrieved: admin_campus_jobs_and_financial_aid.txt, admin_meal_plan_changes.txt, dining_pellew_dining_hall_followup.txt, dining_verrill_street_grill.txt, money_jobs.txt

```
No, you cannot study during your shift at a dining job. 

Source: money_jobs.txt
```

### How often does the campus shuttle run on weekdays? — run 1

- Best distance: 0.4251 (passed the gate)
- Sources retrieved: course_stat_150_workload.txt, dining_kestrel_commons.txt, dining_verrill_street_grill.txt, transit_shuttle.txt, transit_walking.txt

```
The campus shuttle runs a loop every 20 minutes from 7am to 11pm on weekdays (from transit_shuttle.txt).
```

### How often does the campus shuttle run on weekdays? — run 2

- Best distance: 0.4251 (passed the gate)
- Sources retrieved: course_stat_150_workload.txt, dining_kestrel_commons.txt, dining_verrill_street_grill.txt, transit_shuttle.txt, transit_walking.txt

```
The campus shuttle runs a loop every 20 minutes from 7am to 11pm on weekdays (transit_shuttle.txt).
```

### How often does the campus shuttle run on weekdays? — run 3

- Best distance: 0.4251 (passed the gate)
- Sources retrieved: course_stat_150_workload.txt, dining_kestrel_commons.txt, dining_verrill_street_grill.txt, transit_shuttle.txt, transit_walking.txt

```
The campus shuttle runs a loop every 20 minutes from 7am to 11pm on weekdays (transit_shuttle.txt).
```

### Are the midterms curved in CS 210? — run 1

- Best distance: 0.4287 (passed the gate)
- Sources retrieved: course_cs_210.txt, course_cs_210_exams.txt, course_math_220_exams.txt, course_phys_130_exams.txt, course_stat_150_exams.txt

```
Yes, the midterms are curved in CS 210 (sources: `course_cs_210_exams.txt` and `course_cs_210.txt`).
```

### Are the midterms curved in CS 210? — run 2

- Best distance: 0.4287 (passed the gate)
- Sources retrieved: course_cs_210.txt, course_cs_210_exams.txt, course_math_220_exams.txt, course_phys_130_exams.txt, course_stat_150_exams.txt

```
Yes, the midterms are curved in CS 210. 

Source: `course_cs_210.txt` (and `course_cs_210_exams.txt`)
```

### Are the midterms curved in CS 210? — run 3

- Best distance: 0.4287 (passed the gate)
- Sources retrieved: course_cs_210.txt, course_cs_210_exams.txt, course_math_220_exams.txt, course_phys_130_exams.txt, course_stat_150_exams.txt

```
Yes, the midterms are curved in CS 210 (sources: `course_cs_210_exams.txt` and `course_cs_210.txt`).
```
