# v30lr5e7 - LR arm: lr 5e-7 from base (vs v25's 1e-6)

Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-v30lr-run-1 (script scripts/kaggle_kernel_v30lr5e7.py). Exact v25 lowlr recipe from base with lr 5e-7, seeds 4,5 pairing with v25rep's draws. Run under the user's overnight mandate (phonemsg-01M7639R7189XFHFSYR9V7E50R, 2026-11-11 22:02; decisions delegated, morning summary). Closes the LR axis: v29lr showed 2e-6 is worse than 1e-6, so 5e-7 probes the other side.

## Result: lr 5e-7 is the best point on the LR curve - new champion recipe

| arm | seed | best step | best names CER | EVAL500 @best |
|---|---|---|---|---|
| v30lr5e7 (5e-7) | 4 | 500 | 0.8667 | 0.0609 |
| v30lr5e7 (5e-7) | 5 | 250 | 0.8629 | 0.0615 |
| v25rep (1e-6) | 4/5/6 | 125/250/250 | 0.8676 / 0.8657 / 0.8692 | 0.0621 / 0.0548 / 0.0545 |
| v29lr (2e-6) | 4/5 | 125/125 | 0.8755 / 0.8899 | 0.0586 / 0.0590 |
| base | - | - | 0.8928 | 0.0624 |

Mean names CER: 5e-7 = 0.8648, 1e-6 = 0.8675, 2e-6 = 0.8827. Both 5e-7 seeds beat the 1e-6 mean; seed 5 (0.8629) is the best single result recorded. LR curve is monotone over the tested range: lower is better down to 5e-7. DRIVER seed 4/5 exit=0 (verified in log).

## Readings

- The curve may still be descending at 5e-7 (seed 4 peaked at the FINAL eval, step 500 - it had not converged). A 2.5e-7 arm or 5e-7 with more steps is the natural next probe; both cost ~35 min of T4 each.
- Champion-checkpoint decision deferred to the user's morning review: v30's best checkpoints were deleted between seeds (v25rep pattern - only timing JSONs persist). Adopting 5e-7 as champion requires a re-run with checkpoint retention, or a fresh champion-train run.
- best@N is selection on the dev eval; these are achieved scores on one held-out dev set (n=105), not evidence of cause. EVAL500 is separate from the names result.
