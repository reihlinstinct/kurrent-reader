# seg-finetune-v1 (2026-11-10)

Fine-tune kraken blla for MM-class line segmentation. User-approved (phonemsg relay 08:24, "יופי, תאמן"), public-domain data only, Kaggle free GPU.

- Kernel: reihlinstinct/kurrent-seg-finetune-v1 (v2; notebooks/kurrent-seg-finetune-v1.py), T4x2, ~6.4h.
- Data (leakage-safe): train 849 pages MM_1_001+MM_1_002 (parquet 0000-0001), val 120 pages MM_1_005 (0004), test 29 pages MM_1_006 (0005 rg5 - the baseline pages). ENTIRE MM_1_006 held out of training (EVAL500 protection).
- Config: ketos segtrain from blla.mlmodel, --resize union --augment, early stop (lag 8). Stopped epoch 21; BEST epoch 13, val_mean_iu 0.6523.
- Kernel ERROR status = post-training glob bug (wrong checkpoint path), NOT a training failure. Weights recovered from the output snapshot via paged list_kernel_session_output (CLI 1.7.4.5 downloads page 1 only).
- Model: private Kaggle dataset reihlinstinct/kurrent-segv1-lineseg-checkpoint (best_0.6523.safetensors + checkpoint_13).

## Held-out test (29 MM_1_006 pages, bbox IoU>=0.5, local CPU, eval_results.json)
| model | recall | precision |
| baseline blla | 0.9018 | 0.9597 |
| segv1 (epoch 13) | 0.9426 | 0.9835 |

Missed lines cut from 9.8% to 5.7% of 1,639 GT lines (-42% relative). Baseline side reproduced exactly.
