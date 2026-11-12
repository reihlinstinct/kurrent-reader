# e2e-segv1-champ (2026-11-12) - first end-to-end pipeline measurement

Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-e2e-segv1-champ-run-1 (CPU, v2; v1 died on CoreML-only vgsl.load_model - kraken 7 loads safetensors via SegmentationTaskModel.load_model). Run under the overnight mandate (phonemsg-01M7639R7189XFHFSYR9V7E50R).

Pipeline: segv1 (kraken blla fine-tune) detects lines on the 190 EVAL500 pages; v25sweep champion TrOCR reads the seg-detected crops; CER vs GT text. MM_1_006 was never trained on by either model. Decode: model-default beam-4 (identical to training-kernel evals).

## Results (EVAL500, 500 lines, 190 pages)

| measure | value |
|---|---|
| GT-crop recognition CER (pipeline floor) | 0.0609 |
| segv1 line recall on these pages (IoU>=0.5) | 1.000 (500/500 matched, 0 missed) |
| end-to-end CER (seg-detected crops) | 0.0644 |

The full seg->read pipeline costs 0.0035 CER absolute over GT crops. segv1 recall on the 29-page dedicated test set is 0.9426; on the EVAL500 pages (sparse lines, ~2.6/page) coverage is complete.

Claim boundary: achieved scores on the held-out eval sets, not evidence of cause. EVAL500 is separate from the names result.
