# segv2 - seg round 2: 8 diverse projects (2026-11-12)

Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-segv2 (script scripts/kaggle_kernel_segv2.py; the durable copy has the output-dir glob fixed - see below). ~8h T4.

- Data (leakage-safe): train 8 projects x 150 pages (MM_1_001/002/003/004/007/008/009/010, parquet files 0,1,2,3,6,7,8,9), val 120 pages MM_1_005, test 29 pages MM_1_006 (0005 rg5, exact segv1 test pages). MM_1_006 fully held out; MM_1_005 val-only.
- Training: ketos segtrain from blla.mlmodel, --resize union --augment, early stop. Best epoch 13, val_mean_iu 0.6469 (segv1: 0.6523 on 2 projects).
- Kernel ERROR status = post-training glob bug AGAIN (my patch renamed the -o output dir text but the replacement silently missed the two-part string; globs looked in segv2/ while ketos wrote segv1/). Training + best-weight conversion (segv1/best_0.6469.safetensors) succeeded; weights recovered from the session output via paged ApiListKernelSessionOutput.
- Model: private dataset https://www.kaggle.com/datasets/reihlinstinct/kurrent-segv2-lineseg-checkpoint (best_0.6469.safetensors + checkpoint_13-0.6469.ckpt).
- Held-out 29-page IoU eval: CPU kernel reihlinstinct/kurrent-segv2-eval (GPU quota exhausted for the week; v31 champion-train blocked until reset). Numbers pending.
