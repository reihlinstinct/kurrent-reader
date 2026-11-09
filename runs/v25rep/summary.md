# v25rep - v25 recipe replicated with fresh seeds 4/5/6

> **Correction 2026-11-09 (v25beam finding):** all numbers in this record were produced with trocr-kurrent's model-DEFAULT decoding, which is beam-4 + early_stopping + length_penalty 2.0 - not greedy. The column "names CER (best-on-dev)" and all reference points quoted here (v25, v26a, v26b, base) share that same default decode, so the comparisons and the replication verdict stand as decoding-consistent. True-greedy at v25-recipe checkpoints is ~0.022 CER worse (see runs/v25beam).



Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-v25rep-run-1 (script scripts/kaggle_kernel_v25rep.py, commit 2318d40 - exact v25 config, only the seeds changed).

Purpose: test whether v25's 0.8685 was a favorable seed draw or a reproducible effect of the v25 recipe. Same held-out v5 names set (105 cells, 50 held-out IdNrs), same EVAL500 (page MM_1_006, never in training). Per-seed best-on-dev checkpoint selection by names CER, as in v25.

| seed | names CER (best-on-dev, n=105) | EVAL500 CER at best (n=500) | seeds-fit CER (n=12) | train s | total s |
|---|---|---|---|---|---|
| 4 | 0.8676 | 0.0621 | 0.9212 | 1054 | 1980 |
| 5 | 0.8657 | 0.0548 | 0.8827 | 1055 | 1961 |
| 6 | 0.8692 | 0.0545 | 0.8964 | 1059 | 1965 |

**Mean best names CER: 0.8675** (range 0.8657-0.8692) | Mean EVAL500 at best: 0.0571 | Mean seeds-fit: 0.9001

Reference points on the same v5 set: v25 original mean 0.8685, v26a self-train 0.8835, v26b aug 0.8852, v27 sched-samp greedy 0.8921, no-training base 0.8928.

Reading: the v25 recipe replicates. Three fresh seeds land at 0.8657-0.8692, bracketing the original v25 run's 0.8685 and clearly separated from base (0.8928) by ~0.025. The v25 result was not a lucky seed draw; the recipe-level improvement over base reproduced on independent seeds. v26a/v26b/v27 remain worse than the v25 recipe on this dev selection.

best@N is selection on the dev eval; these are achieved scores on one held-out dev set, not evidence of cause. EVAL500 (page MM_1_006) was never in training and is separate from this names result; seeds-fit (n=12) is a third, smaller eval.

Config: lr 1e-6, warmup 100, 2 epochs, batch 8, eval every 125 steps, max 500 steps, left_out MM_1_006, no checkpoint init (resume from v25 recipe base). Train line-samples per seed: 63693, pages 1478. ~33 min per seed on T4.
