# v25 names run (kurrent-namesv5-run-2)

v24 + assert fix (KURRENT_EXPECT_CELLS 306 -> 216). Eval set: v5 FINAL, 105 cells / 49 eval persons / 50 held-out IdNrs (experiments/2026-10-23/eval_names_v5.jsonl). Selection = names CER on 53 scored cells (name+occupation); 50 date cells scored by span_hit. EVAL500 = MM_1_006 500-line held-out page, never in training.

Config per seed: lr 1e-6, warmup 100, 2 epochs, eval_every 125, batch 8, max_steps 500, 63693 samples, 1478 pages.

## Best-checkpoint results (best@step on dev names CER)

| seed | best step | names CER (105) | v4subset CER | span_hit | EVAL500 CER | EVAL500 word_acc |
|---|---|---|---|---|---|---|
| 1 | 250 | 0.8657 | 0.9170 | 0.0421 | 0.0549 | 0.7722 |
| 2 | 125 | 0.8701 | 0.9067 | 0.0105 | 0.0621 | 0.7396 |
| 3 | 250 | 0.8697 | 0.8790 | 0.0105 | 0.0546 | 0.7723 |
| mean | | 0.8685 | 0.9009 | 0.0210 | 0.0572 | 0.7614 |

v24 reference (same 105-cell set): names CER 0.8928, v4subset 0.9067, span_hit 0.0, EVAL500 0.0624 / 0.7372.

Claim boundary: achieved scores, not causation; best@N is selection on the dev eval; EVAL500 reported separately from the names result.
