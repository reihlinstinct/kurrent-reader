# v27 - scheduled sampling (SS_P=0.15) + beam-4 eval of checkpoint-best (run 2)

Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-v27-schedsamp-run-2 (script scripts/kaggle_kernel_v27.py, commit e610c9b - fixes the DataParallel unwrap crash that killed run 1 on all 3 seeds when Kaggle assigned T4 x2).

Held-out v5 names set (105 cells, 50 held-out IdNrs). Per-seed best-on-dev checkpoint selection by greedy names CER; beam-4 decode of the same checkpoint measured alongside. EVAL500 untouched.

| seed | best step | names CER greedy (best-on-dev) | names CER beam-4 (same ckpt) | EVAL500 CER at best |
|---|---|---|---|---|
| 1 | 500 | 0.8882 | 0.8717 | 0.0492 |
| 2 | 375 | 0.8893 | 0.8752 | 0.0520 |
| 3 | 125 | 0.8988 | 0.8719 | 0.0635 |

**Mean best names CER (greedy): 0.8921** | **Mean best names CER (beam-4): 0.8729**

Reference points on the same v5 set (greedy): v25 mean 0.8685, v26a self-train 0.8835, v26b aug 0.8852, no-training base 0.8928.

Reading: scheduled sampling at p=0.15 landed at base level on greedy (0.8921 vs base 0.8928), worse than v25 0.8685 and both v26 arms on this dev selection. Beam-4 at the same checkpoints improved over greedy in every seed (-0.017 to -0.027 CER) but still does not reach v25's greedy number. Beam-4 on v25's own checkpoints cannot be tested (v25 checkpoints were deleted between seeds).

best@N is selection on the dev eval; these are achieved scores on one held-out dev set, not evidence of cause. Beam-4 vs greedy is a within-checkpoint decoding comparison on the same dev set. EVAL500 (page MM_1_006) was never in training and is separate from this names result.

Config: lr 1e-6, 2 epochs, batch 8, eval every 125 steps, max 500 steps, ss_p 0.15, left_out MM_1_006. Train line-samples per seed: 63693, pages 1478.
