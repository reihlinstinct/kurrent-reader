# Plan + outcome: kraken blla fine-tune on MM-class pages

Goal was to lift line recall on MM_1_006-style pages from 0.902 toward >=0.97 without touching recognition training or contaminating EVAL500.

Split (leakage-safe): train MM_1_001..MM_1_002, val MM_1_005, test MM_1_006 (entire project held out of training).

Outcome (seg-finetune-v1, 2026-11-10): recall 0.9018 -> 0.9426, precision 0.9597 -> 0.9835 on 29 held-out MM_1_006 pages. Best epoch 13 of 21 (early stop), val_mean_iu 0.6523. Model: private dataset reihlinstinct/kurrent-segv1-lineseg-checkpoint.

Not done / possible round 2: more train pages (only 2 of ~300 projects used), longer training, region-class cleanup, narrative-page end-to-end eval. Roboflow path obsolete for this use case.
