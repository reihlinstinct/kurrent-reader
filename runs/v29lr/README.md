# v29lr - LR arm: lr 2e-6 from base (vs v25's 1e-6)

Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-v29lr-run-1 (script scripts/kaggle_kernel_v29lr.py). Exact v25 lowlr recipe from base with lr 2e-6 (v25 = 1e-6; v8-v12 = 5e-6 which the v13 gentle block replaced), seeds 4,5 pairing with v25rep's draws. Question: is 1e-6 the right point on the LR curve?

## Result: lr 2e-6 is worse; peaks at the first eval

| arm | seed | best step | best names CER | EVAL500 @best |
|---|---|---|---|---|
| v29lr (2e-6) | 4 | 125 | 0.8755 | 0.0586 |
| v29lr (2e-6) | 5 | 125 | 0.8899 | 0.0590 |
| v25rep (1e-6) | 4/5/6 | 125/250/250 | 0.8676 / 0.8657 / 0.8692 | 0.0621 / 0.0548 / 0.0545 |
| base | - | - | 0.8928 | 0.0624 |

Both 2e-6 seeds peaked at step 125 (the FIRST eval) and degraded afterwards; the 1e-6 recipe peaks at 125-250 with better scores. Seed spread at 2e-6 (0.8755 vs 0.8899) is wider than at 1e-6.

## Readings

- LR curve now has three points: 5e-6 (v8-v12, regressed), 2e-6 (worse: mean 0.8827), 1e-6 (champion: mean 0.8675). 1e-6 remains the best point tested; the direction of improvement, if any, would be LOWER lr, not higher.
- v4-subset CER at 2e-6 seed 5 (1.0108) shows the hotter LR destabilizes part of the dev set even when the headline CER improves over base.

best@N is selection on the dev eval; these are achieved scores on one held-out dev set (n=105), not evidence of cause. EVAL500 is separate from the names result.
