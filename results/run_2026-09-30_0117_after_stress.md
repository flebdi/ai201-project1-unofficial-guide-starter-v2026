# Run log — after_stress

- Produced by: `run_eval.py::main`
- Retrieval: `store.py::search`, chunks from `chunker.py::split_documents`
- Corpus: `campus_life` (index variant `default`)
- top-k: 5 · relevance cutoff: 0.6
- Question set: STRESS_QUESTIONS (unit 2 stress set, not graded)
- Runs per question: 3, caching off
- When: 2026-09-30 01:17

This table is one row per QUESTION. The run log your README asks for is
one row per CRITERION, so aggregate these into it — criterion 1 is how many
of your questions had the answer in the retrieved chunks, and so on.

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| How are juniors and seniors prioritized in the housing lottery? | pass | pass | pass |
| What happens if a student wants to add or drop a course after the deadline? | fail | fail | fail |
| does work-study job count toward your financial aid the same way a nomral non work study job does? | pass | pass | pass |
| What is the workload like for CS 210? | pass | pass | pass |
| What are the laundry conditions at Aldridge Hall? | pass | pass | pass |

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

### How are juniors and seniors prioritized in the housing lottery? — run 1

- Best distance: 0.2050 (passed the gate)
- Sources retrieved: admin_housing_lottery.txt, advising_registration.txt, course_stat_150_exams.txt, dining_the_atrium_followup.txt, housing_tamsin_court.txt

```
Juniors and seniors are ordered by accumulated credit hours first, with ties broken randomly. 

Documents used: `admin_housing_lottery.txt`
```

### How are juniors and seniors prioritized in the housing lottery? — run 2

- Best distance: 0.2050 (passed the gate)
- Sources retrieved: admin_housing_lottery.txt, advising_registration.txt, course_stat_150_exams.txt, dining_the_atrium_followup.txt, housing_tamsin_court.txt

```
Juniors and seniors are ordered by accumulated credit hours first in the housing lottery, with any ties broken randomly. 

Sources used: `admin_housing_lottery.txt`
```

### How are juniors and seniors prioritized in the housing lottery? — run 3

- Best distance: 0.2050 (passed the gate)
- Sources retrieved: admin_housing_lottery.txt, advising_registration.txt, course_stat_150_exams.txt, dining_the_atrium_followup.txt, housing_tamsin_court.txt

```
Juniors and seniors in the housing lottery are ordered by accumulated credit hours first, with any ties broken randomly. 

Document used: `admin_housing_lottery.txt`
```

### What happens if a student wants to add or drop a course after the deadline? — run 1

- Best distance: 0.2924 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, admin_declaring_a_major.txt, admin_grade_appeals.txt, admin_pass_fail_option.txt, admin_withdrawal_deadline.txt

```
The provided documents do not contain information on what happens if a student wants to add or drop a course *after* the respective deadlines (the end of the second week for adding, and the end of week six for dropping). 

Documents used: `admin_add_drop_deadline.txt`
```

### What happens if a student wants to add or drop a course after the deadline? — run 2

- Best distance: 0.2924 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, admin_declaring_a_major.txt, admin_grade_appeals.txt, admin_pass_fail_option.txt, admin_withdrawal_deadline.txt

```
Based on the provided documents, you can add a course through the end of the second week, and you can drop a course through the end of week six (though a drop after week two shows as a "W" on your transcript). The documents do not state what happens if a student attempts to add or drop a course *after* these respective deadlines. 

Documents used: `admin_add_drop_deadline.txt` and `admin_withdrawal_deadline.txt`.
```

### What happens if a student wants to add or drop a course after the deadline? — run 3

- Best distance: 0.2924 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, admin_declaring_a_major.txt, admin_grade_appeals.txt, admin_pass_fail_option.txt, admin_withdrawal_deadline.txt

```
Based on the provided documents:

* You can add a course through the end of the second week (admin_add_drop_deadline.txt). The documents do not state what happens if a student tries to add a course *after* this deadline.
* Dropping a course is allowed through the end of week six, though a drop after week two results in a "W" on your transcript (admin_add_drop_deadline.txt, admin_withdrawal_deadline.txt). The documents do not state what happens if a student tries to drop a course *after* the week six deadline.

Documents used: admin_add_drop_deadline.txt, admin_withdrawal_deadline.txt
```

### does work-study job count toward your financial aid the same way a nomral non work study job does? — run 1

- Best distance: 0.2475 (passed the gate)
- Sources retrieved: admin_campus_jobs_and_financial_aid.txt, admin_study_abroad.txt, course_cs_340.txt, course_engl_205_exams.txt, money_jobs.txt

```
No, work-study earnings do not count against your financial aid the way ordinary (non-work-study) income does. Non-work-study campus jobs do count against your financial aid. (Source: admin_campus_jobs_and_financial_aid.txt)
```

### does work-study job count toward your financial aid the same way a nomral non work study job does? — run 2

- Best distance: 0.2475 (passed the gate)
- Sources retrieved: admin_campus_jobs_and_financial_aid.txt, admin_study_abroad.txt, course_cs_340.txt, course_engl_205_exams.txt, money_jobs.txt

```
No, work-study earnings do not count against your financial aid the way ordinary income does, whereas non-work-study campus jobs do count. 

Source used: `admin_campus_jobs_and_financial_aid.txt`
```

### does work-study job count toward your financial aid the same way a nomral non work study job does? — run 3

- Best distance: 0.2475 (passed the gate)
- Sources retrieved: admin_campus_jobs_and_financial_aid.txt, admin_study_abroad.txt, course_cs_340.txt, course_engl_205_exams.txt, money_jobs.txt

```
No, work-study earnings do not count against your financial aid the way ordinary income does, whereas non-work-study campus jobs do count. 

Documents used: *admin_campus_jobs_and_financial_aid.txt*
```

### What is the workload like for CS 210? — run 1

- Best distance: 0.2762 (passed the gate)
- Sources retrieved: course_cs_210_workload.txt, course_cs_340_workload.txt, course_hist_118_workload.txt, course_phys_130_workload.txt, course_stat_150_workload.txt

```
The workload for CS 210 Data Structures is 8 to 10 hours a week outside of class. It is front-loaded, meaning the first month is heavier than the rest. 

Source: course_cs_210_workload.txt
```

### What is the workload like for CS 210? — run 2

- Best distance: 0.2762 (passed the gate)
- Sources retrieved: course_cs_210_workload.txt, course_cs_340_workload.txt, course_hist_118_workload.txt, course_phys_130_workload.txt, course_stat_150_workload.txt

```
The workload for CS 210 Data Structures is 8 to 10 hours a week outside of class (real time, not optimistic time). It is also front-loaded, meaning the first month is heavier than the rest, partly because you are learning the format. 

Sources used: `course_cs_210_workload.txt`
```

### What is the workload like for CS 210? — run 3

- Best distance: 0.2762 (passed the gate)
- Sources retrieved: course_cs_210_workload.txt, course_cs_340_workload.txt, course_hist_118_workload.txt, course_phys_130_workload.txt, course_stat_150_workload.txt

```
The workload for CS 210 Data Structures is 8 to 10 hours a week outside of class (real time, not optimistic). It is also front-loaded, meaning the first month is heavier than the rest. 

Source: `course_cs_210_workload.txt`
```

### What are the laundry conditions at Aldridge Hall? — run 1

- Best distance: 0.3330 (passed the gate)
- Sources retrieved: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_innisfree_hall.txt, housing_innisfree_hall_laundry.txt, housing_tamsin_court.txt

```
At Aldridge Hall, laundry costs $1.75 to wash and $1.50 to dry, and it is card only. There are eight washers and six dryers, which is an incorrect ratio causing dryers to back up on Sunday evenings. The best times to do laundry are Tuesday or Wednesday morning, and you will have to wait on Sundays after 6 pm. 

Documents used: `housing_aldridge_hall_laundry.txt`, `housing_aldridge_hall.txt`
```

### What are the laundry conditions at Aldridge Hall? — run 2

- Best distance: 0.3330 (passed the gate)
- Sources retrieved: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_innisfree_hall.txt, housing_innisfree_hall_laundry.txt, housing_tamsin_court.txt

```
At Aldridge Hall, laundry costs $1.75 to wash and $1.50 to dry, and it is card only. There are eight washers and six dryers, which is an incorrect ratio causing dryers to back up on Sunday evenings. The best times to do laundry are Tuesday or Wednesday mornings, while waiting is likely on Sundays after 6 pm. 

Sources: `housing_aldridge_hall_laundry.txt` and `housing_aldridge_hall.txt`
```

### What are the laundry conditions at Aldridge Hall? — run 3

- Best distance: 0.3330 (passed the gate)
- Sources retrieved: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_innisfree_hall.txt, housing_innisfree_hall_laundry.txt, housing_tamsin_court.txt

```
At Aldridge Hall, laundry costs $1.75 for a wash and $1.50 for a dry, and it is card only. There are eight washers and six dryers, which leads to a wrong ratio where dryers back up on Sunday evenings, making Tuesday or Wednesday morning the best time to do laundry. 

Sources: `housing_aldridge_hall_laundry.txt`, `housing_aldridge_hall.txt`
```
