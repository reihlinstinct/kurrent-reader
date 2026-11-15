# v32ext - extended multi-seed on the v31 champion recipe (1000 steps)

Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-v32ext-run-1 (script = v31champ script with seeds 6,7,8,9 and MAX_STEPS 1000). User approved 2026-11-14 23:45 ("תתחיל", phonemsg-01M7E0BCVRV43WZZK596VH2ZTB, via parent) as the answer to "anything else worth training". Free Kaggle quota only.

Question: v31 seed4 was still improving at step500 (0.8667) while seed5 peaked @250 (0.8629) - does the lr 5e-7 regime keep improving past 500, and can fresh seeds beat the 0.8629 champion?

## Answer: peaks stay early (250-375); no gains past 500. New champion seed9@375, names CER 0.8600.

| seed | best step | best names CER | EVAL500 (mm006_500) @best | train s | total s |
|---|---|---|---|---|---|
| 6 | 250 | 0.8668 | - | 1940 | 2712 |
| 7 | 250 | 0.8677 | - | - | - |
| 8 | 375 | 0.8652 | 0.0584 | - | - |
| 9 | 375 | **0.8600** | **0.0581** | 1940 | 2712 |

(all timing JSONs in this directory; seed6/7 rows above from their JSONs)

- Champion per protocol (min names CER): **seed9 @ step375, 0.8600** vs v31 champion 0.8629. Margin 0.0029 is within seed noise - best@N is selection on the dev eval - but the independent always-held-out EVAL500@best moves the same direction (0.0581 vs v31's 0.0609/0.0615).
- Verified: sha256(champion/model.safetensors) == sha256(checkpoint-best-seed9/model.safetensors) = 9300cc447ab90a536422cea0bc97acd02d626c1b4de1eb6ce7ab9e26d2d2e7ac.
- Decode pinned in artifact: num_beams 4, early_stopping, length_penalty 2.0, max_length 128 (comparable to all evals since v27).
- All 4 seeds completed (per-seed timing JSONs + checkpoint-best-seedN dirs in kernel output).

## Artifacts

- New champion (HF layout, private dataset): https://www.kaggle.com/datasets/reihlinstinct/kurrent-v32champ-checkpoint - config.json, generation_config.json, model.safetensors (1.34 GB), preprocessor_config.json, training_args.bin, timing_result_seed6-9.json. v31 champion dataset left untouched as the v31 record.
- Kernel output also carries checkpoint-best-seed6..9/ full checkpoints (kernel-side only).

## Notes

- Extending 500 -> 1000 steps: no seed improved past 375. The productive regime at 5e-7 is 250-375; the extra GPU bought certainty, not score. Future runs should cap at 500 and spend on seeds instead.
- achieved scores on one held-out dev set (n=105 names; EVAL500 n=500, page MM_1_006 never trained on), not evidence of cause.
