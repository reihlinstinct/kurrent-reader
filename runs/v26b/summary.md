# v26b - hand-diversity augmentation (run 1)

Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-v26b-aug-run-1 (script scripts/kaggle_kernel_v26b.py, commit 20c7e4e)

Held-out v5 names set (105 cells, 50 held-out IdNrs). Per-seed best-on-dev checkpoint selection; EVAL500 untouched.

| seed | best step | names CER (best-on-dev) | train s | total s |
|---|---|---|---|---|
| 1 | 250 | 0.8849 | 935 | 1756 |
| 2 | 125 | 0.8826 | 931 | 1721 |
| 3 | 125 | 0.8880 | 931 | 1722 |

**Mean best names CER: 0.8852**

Reference points on the same v5 set: v25 mean 0.8685, no-training base 0.8928.

Reading: v26b lands between v25 and base on this dev selection - better than the untrained base, worse than v25 on this run.
best@N is selection on the dev eval; these are achieved scores on one held-out dev set, not evidence of cause. EVAL500 (page MM_1_006) was never in training and is separate from this names result.

Train samples per seed: 63693 (augmented), pages: 1478, config: lr 1e-6, 2 epochs, batch 8, eval every 125 steps, max 500 steps, left_out MM_1_006.
