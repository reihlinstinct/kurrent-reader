# v26a - self-training on unlabeled pages (run 1)

Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-v26a-selftrain-run-1 (script scripts/kaggle_kernel_v26a.py)

Held-out v5 names set (105 cells, 50 held-out IdNrs). Per-seed best-on-dev checkpoint selection; EVAL500 untouched.

| seed | best step | names CER (best-on-dev) | train s | total s |
|---|---|---|---|---|
| 1 | 250 | 0.8832 | 979 | 1832 |
| 2 | 125 | 0.8926 | 976 | 1796 |
| 3 | 250 | 0.8747 | 979 | 1804 |

**Mean best names CER: 0.8835**

Reference points on the same v5 set: v25 mean 0.8685, v26b mean 0.8852, no-training base 0.8928.

Reading: v26a lands between v25 and base on this dev selection - better than the untrained base and marginally better than v26b, worse than v25 on this run. Neither v26 variant closes the gap to v25; the v25 failure-mode analysis (zero near-misses, prior-driven hallucination on unseen hands) stands as the bottleneck description.
best@N is selection on the dev eval; these are achieved scores on one held-out dev set, not evidence of cause. EVAL500 (page MM_1_006) was never in training and is separate from this names result. Held-out h12 IdNr cells are unchanged vs base (h01 0.929), consistent with no held-out leakage.

Train samples per seed: 63693 (labeled + pseudo-labeled), pages: 1478, config: lr 1e-6, 2 epochs, batch 8, warmup 100, eval every 125 steps, max 500 steps, left_out MM_1_006.
