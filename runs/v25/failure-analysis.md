# v25 per-cell failure analysis (2026-11-08)

Basis: runs/v25/timing_result_seed{1,2,3}.json (best checkpoint per seed, selection = names CER on dev eval), joined with experiments/2026-10-23/eval_names_v5.jsonl (105 cells: 50 name, 50 date, 5 occupation; eval_src splits: v4-original 5 persons/7 cells, existing-heldout-person 4 persons/8 cells, new-heldout-person 44 persons/90 cells).

## Headline

v24's 0.8928 was the BASE model's boot eval (v24 failed fast before training). v25 trained: mean names CER 0.8685. So fine-tuning (2 epochs, 63693 samples) bought ~2.4 CER points on the identical 105-cell set, with the train set ~10% smaller after decontaminating the 44 new held-out persons.

## CER by eval_src x kind (pooled over 3 seeds)

- new-heldout-person names (n=132 cell-evals): 0.8590
- existing-heldout-person names (n=12): 0.9247
- v4-original names (n=3): 0.7707
- v4-original occupations (n=15): 0.9269 (worst group)

The 44 new persons are NOT harder than the original held-out set; enlarging the dev set did not dilute the metric with easy cells. Occupation cells remain the hardest category.

## Failure character

1. No near-misses at all. 0/162 name+occupation cell-evals land within 4 character edits of the reference. Failures are total content misses, not orthographic slips. The model cannot read these hands; it is not "almost" reading them.
2. Prior-driven hallucination sinks. Most repeated hypotheses: "xx" 18x, "Ed . Fenzl" 7x, "." 6x, "Hofburg" 4x, "Marga" 4x - none ever matching the reference. Frequent corpus tokens are emitted regardless of image content.
3. Even the "best" cells are morpheme luck: best cell is CER 0.571 ("Besbacher 2" vs ref "Jeta Mosbacher") - the model latches onto the register's dominant surname morpheme ("...bacher", the Mosbacher family cluster) and common endings ("-ette"). CER 0.6-0.8 cells are partial letter overlap by frequency, not reading.
4. No length effect: short/mid/long refs all ~0.85-0.88 mean CER. Not a cropping/length problem.
5. Seed agreement 48/103 cells identical hyp across seeds - the wrong answers are stable, i.e. systematic, not sampling noise.
6. Dates: span_hit 5/396 pooled cell-evals (all 5 on new-heldout persons, likely chance token overlap). Date reading remains unsolved and is a different failure mode than names.

## Implications for v26 (options, no decision taken)

A. The bottleneck is visual generalization to unseen hands, not label quality: near-zero near-miss rate means more/better labels of the same kind won't move names CER much. Options that target the actual bottleneck: pretraining-style domain adaptation on unlabeled register pages (masked/self-supervised), or augmentation aimed at hand diversity.
B. Occupation cells (0.9269) and long multi-word names fail hardest in absolute terms; a cell-type-specific head or curriculum is unlikely to help given (1).
C. Dates need a different mechanism entirely (span extraction is 0.01-0.04); keep scoring separately.

Claim boundary: achieved scores on the dev eval, not causation; best@N is selection on dev; EVAL500 (0.0572 mean CER) is reported separately and stays strong, so the names-domain gap is specific to the held-out writers, not global degradation.
