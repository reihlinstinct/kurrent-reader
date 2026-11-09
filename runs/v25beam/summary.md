# v25beam - v25 recipe, first explicit-decoding eval: true greedy vs beam-4 at checkpoint-best

Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-v25beam-run-1 (script scripts/kaggle_kernel_v25beam.py, commit 3b6e9aa). Seeds 4,5,6, exact v25 recipe.

## The finding: every pre-v27 eval was beam-4, not greedy

dh-unibe/trocr-kurrent's generation_config defaults to **num_beams=4, early_stopping=true, length_penalty=2.0**. All scripts before v27 called `model.generate(pixels, max_length=64)` with no `num_beams` argument, so every earlier number on record - v25 0.8685, v25rep 0.8675, v26a 0.8835, v26b 0.8852, and the no-training base 0.8928 - was produced with **model-default beam-4 decoding**, not greedy. v27 introduced the explicit `num_beams` parameter; v25beam is the first run to measure the v25 recipe under both decodings explicitly.

| seed | best step (selected by true greedy) | names CER TRUE GREEDY (n=105) | names CER beam-4, same ckpt (n=105) | EVAL500 CER (true greedy) |
|---|---|---|---|---|
| 4 | 250 | 0.8953 | 0.8753 | 0.0560 |
| 5 | 125 | 0.8913 | 0.8709 | 0.0640 |
| 6 | 250 | 0.8937 | 0.8692 | 0.0562 |

**Mean true greedy: 0.8934** | **Mean beam-4: 0.8718** | Mean EVAL500: 0.0587

## What changes and what survives

- **Decoding effect at v25-recipe checkpoints: beam-4 beats true greedy by ~0.022 CER** (0.8718 vs 0.8934). This is as large as the v25 training effect. The model's own default decode (beam-4) is doing half the work in the headline numbers.
- **v25 training effect survives, decoding-controlled**: v25/v25rep/base were all default beam-4, so v25's ~-0.025 vs base (0.8675-0.8685 vs 0.8928) was measured at constant decoding. It stands.
- **v25-vs-v27 gap narrows under matched decoding**: previously stated as v25 0.8685 vs v27 "greedy" 0.8921 (cross-decoding, misleading). Under identical beam-4: v25 recipe 0.8675 (beam-4-selected ckpts) / 0.8718 (greedy-selected ckpts) vs v27 beam-4 0.8729. v25 still ahead, by ~0.001-0.005. v27's forced true greedy (0.8921) matches v25beam's (0.8934) - cross-run consistent.
- **Selection decode changed this run**: v25/v25rep selected best-on-dev with default beam-4; v25beam selected with true greedy (the beam-4 column here is beam-4 at greedy-selected checkpoints). The 0.8675 vs 0.8718 difference is consistent with selection-decode mismatch plus checkpoint noise.
- **EVAL500 not cross-comparable this run**: v25beam's EVAL500/h12/seeds-fit evals ran true greedy (0.0587 mean); all prior EVAL500 numbers were default beam-4 (v25rep 0.0571). Difference is small but the decode differs.
- **Never measured**: base model under true greedy. The base column (0.8928) is default beam-4 only.

Practical rule going forward: every eval must pin its decoding explicitly (num_beams, early_stopping, length_penalty) and record it in the timing JSON; default decode of trocr-kurrent is beam-4/early-stopping/lp-2.0.

best@N is selection on the dev eval; these are achieved scores on one held-out dev set, not evidence of cause. Beam-4 vs greedy here is a within-checkpoint decoding comparison on the same dev set. EVAL500 (page MM_1_006) was never in training and is separate from the names result.
