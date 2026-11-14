# v31champ - champion-train at lr 5e-7 WITH checkpoint retention

Kernel: https://www.kaggle.com/code/reihlinstinct/kurrent-v31champ-run-1 (script scripts/kaggle_kernel_v31champ.py). Approved by parent 2026-11-11 23:18 under the user's overnight mandate (phonemsg-01M7639R7189XFHFSYR9V7E50R): rerun v30's winning recipe (lr 5e-7, seeds 4/5, from base) keeping the best checkpoints, so the champion model actually exists as an artifact. v30 deleted checkpoints between seeds; v31 retains them.

Pushed 2026-11-14 04:11 IST after the weekly GPU quota reset (quota had been exhausted since 2026-11-12 07:31; one push attempt per 4h wake until it went through). Free Kaggle quota only.

## Result: champion = seed5 @ step 250, names CER 0.8629 (matches v30 exactly)

| seed | best step | best names CER | EVAL500 @best | train s | total s |
|---|---|---|---|---|---|
| 4 | 500 | 0.8667 | 0.0609 | 979 | 1802 |
| 5 | 250 | 0.8629 | 0.0615 | 969 | 1757 |

Identical to v30 (seed4 0.8667@500, seed5 0.8629@250): the recipe reproduces bit-for-bit on the metric level. Champion checkpoint selected by DRIVER = seed5's best (lower CER). Verified: sha256 of champion/model.safetensors == checkpoint-best-seed5/model.safetensors (77dcc13d...). Both seeds completed (timing JSONs + full checkpoints present).

Decode: generation_config pinned in the artifact - num_beams 4, early_stopping, length_penalty 2.0, max_length 128 (the decode used by all evals since v27; selection metric comparable to history).

## Artifacts

- Champion (HF layout, private dataset, all files one version): https://www.kaggle.com/datasets/reihlinstinct/kurrent-v31champ-checkpoint
  - config.json, generation_config.json, model.safetensors (1.34 GB), preprocessor_config.json, training_args.bin, timing_result_seed4.json, timing_result_seed5.json
- Kernel output also carries checkpoint-best-seed4/ and checkpoint-best-seed5/ full checkpoints (kernel-side only).

## Notes

- best@N is selection on the dev eval; achieved scores on one held-out dev set (n=105 names; EVAL500 n=500, page MM_1_006 never trained on), not evidence of cause.
- Champion readiness for the app/pipeline: this is the recognition model to pair with segv1 (e2e CER 0.0644 vs GT-crop floor 0.0609, runs/e2e-segv1-champ). segv2 (0.9475/0.9786) missed its target and stays behind segv1.
