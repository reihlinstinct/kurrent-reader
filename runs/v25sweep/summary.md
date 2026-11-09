# v25sweep - decode matrix at one kept v25-recipe checkpoint + base under true greedy

Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-v25sweep-run-1 (script scripts/kaggle_kernel_v25sweep.py, commit daea0ea). One seed (4), checkpoint-best KEPT and archived in private dataset reihlinstinct/kurrent-v25sweep-checkpoint for reuse (use with the dh-unibe/trocr-kurrent processor).

Every eval pinned and recorded its decode config. Selection protocol = model-default beam-4 (early_stopping, length_penalty 2.0), matching v25/v25rep history. Names set = v5 held-out (105 cells, 50 held-out IdNrs). EVAL500 (MM_1_006) never trained on.

## Decode matrix: names CER (n=105), base vs trained best (step 125)

| decode | base (no training) | v25-recipe best |
|---|---|---|
| true greedy (beams=1) | 0.9104 | 0.8972 |
| beam2 | 0.8946 | 0.8731 |
| beam4 default (es, lp 2.0) | 0.8928 | **0.8676** |
| beam4, lp 1.0 | 0.8952 | 0.8738 |
| beam4, lp 0.6 | 0.8967 | 0.8770 |
| beam6 | 0.8863 | 0.8681 |

## Readings

- **Open cell filled**: base under true greedy = 0.9104. Full decomposition at the trained checkpoint: base greedy 0.9104 -> trained greedy 0.8972 (training, at greedy: -0.013) -> trained beam-4 0.8676 (decoding: -0.030). At beam-4 the training effect is larger: 0.8928 -> 0.8676 = -0.025. Beam decoding helps the trained model more than the base (-0.030 vs -0.018).
- **The model's default decode is already optimal** at the trained checkpoint: beam-4 + early stopping + lp 2.0 wins (0.8676); beam-6 ties within noise (0.8681); relaxing the length penalty (1.0 / 0.6) makes it worse. No decode change recommended.
- **Exact cross-run reproducibility**: this seed-4 beam-4-selected best (step 125, 0.8676) matches v25rep seed 4 (0.8676) to 4 decimals. Combined with v25beam (greedy selection -> step 250, 0.8753 under beam-4), the earlier "greedy collapse" is fully explained: it was selection-decode mismatch (checkpoints chosen for greedy are worse under beam-4), not training nondeterminism.
- EVAL500 at best 0.0621 vs base 0.0624 (both beam-4 default, history-comparable): the names-set gains do not move the untouched 500-cell page eval.

best@N is selection on the dev eval; these are achieved scores on one held-out dev set (n=105), not evidence of cause. Base vs best is a training comparison at constant decode per row; rows are decoding comparisons at constant model. EVAL500 is separate from the names result.
