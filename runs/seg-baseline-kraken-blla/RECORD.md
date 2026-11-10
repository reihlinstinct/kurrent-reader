# seg-baseline-kraken-blla (2026-11-10)

Baseline: is text-line detection a bottleneck for end-to-end Kurrent transcription?

- Detector: kraken 7.1.1 blla.segment, generic model blla.mlmodel (Zenodo 22879549), CPU.
- Data: 29 pages of MM_1_006 (HF dh-unibe/image-text_kurrent-xix, parquet train/0005 row group 5), GT from PageXML (1,639 lines). Public domain (State Archives of Zurich).
- Scoring: bbox IoU >= 0.5 between predicted and GT lines.

## Result
- Recall 0.9018, precision 0.9597 (pred 1540 vs 1639 GT). Reproduced identically in the segv1 eval rerun.
- ~1 in 10 GT text lines never reaches recognition end-to-end; all existing metrics (EVAL500, dev evals) use GT/manual crops, so this loss is invisible to them.
- Conclusion: line detection is a real, measurable bottleneck for narrative/end-to-end use.
