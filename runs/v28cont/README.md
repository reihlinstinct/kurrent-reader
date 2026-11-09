# v28cont - continuation arm: +500 steps from the champion checkpoint

Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-v28cont-run-1 (script scripts/kaggle_kernel_v28cont.py). Resumed from the v25sweep champion (seed-4 step-125, names CER 0.8676, private dataset reihlinstinct/kurrent-v25sweep-checkpoint) and trained +500 steps at the unchanged v25 lowlr recipe (lr 1e-6, warmup 100, batch 8, eval every 125), seeds 4,5. Question: is the v25 recipe undertrained at 500 steps?

## Result: clean negative

| seed | start (before) names CER | best step | best names CER |
|---|---|---|---|
| 4 | 0.8676 | none | no step beat the start |
| 5 | 0.8676 | none | no step beat the start |

Keep-best is baseline-initialized (a step must beat the starting checkpoint's 0.8676 to be recorded). Neither seed produced a step better than the champion it started from, so no checkpoint-best was saved and nothing was archived. EVAL500 (MM_1_006, never trained on) at the start checkpoint: 0.0621, matching v25sweep.

## Readings

- The v25 recipe is NOT undertrained at 500 steps: continuing from its best point at the same LR does not improve the dev score on either seed.
- Caveat (adaptive selection): continuing from a dev-selected checkpoint and re-selecting on the same dev adds selection pressure; EVAL500 remains the untouched check and was not moved by continuation (start 0.0621).
- Champion unchanged: reihlinstinct/kurrent-v25sweep-checkpoint (v25rep seed-4 step-125, 0.8676).

best@N is selection on the dev eval; these are achieved scores on one held-out dev set (n=105), not evidence of cause.
