# kurrent-segv2-eval: 29-page held-out IoU eval of segv2 (best_0.6469) on CPU.
# Same protocol and same 29 MM_1_006 pages as segv1 (recall 0.9426 / precision 0.9835,
# base blla 0.9018 / 0.9597) -> direct comparison. GPU quota is exhausted; CPU only.
# segv2's training kernel errored post-training (output-dir glob); training + weights fine.
import subprocess, os, json, time

def sh(cmd):
    print("+", cmd, flush=True)
    r = subprocess.run(cmd, shell=True)
    if r.returncode != 0:
        raise RuntimeError("failed: " + cmd)

sh("pip install -q --no-deps kraken==7.1.1")
sh("pip install -q lightning htrmopo cattrs shapely scikit-image jsonschema lxml python-bidi coremltools fsspec requests safetensors iso639-lang scikit-learn scipy threadpoolctl \"click<8.3\" pyarrow")

from kraken import blla
from kraken.tasks import SegmentationTaskModel
from lxml import etree
from PIL import Image
import pyarrow.parquet as pq
import pyarrow as pa
import fsspec
import glob as _glob
print("imports OK", flush=True)

W = "/kaggle/working"
SEG_HITS = _glob.glob("/kaggle/input/**/best_0.6469.safetensors", recursive=True)
print("seg model hits:", SEG_HITS, flush=True)
assert SEG_HITS
task = SegmentationTaskModel.load_model(SEG_HITS[0])
seg_model = task.seg_models[0]
if not getattr(seg_model, "user_metadata", None) or "hyper_params" not in seg_model.user_metadata:
    if not getattr(seg_model, "user_metadata", None):
        seg_model.user_metadata = {}
    seg_model.user_metadata["hyper_params"] = {}

# test: MM_1_006 file 0005 row group 5 (the exact 29 segv1 test pages)
BASE = "https://huggingface.co/datasets/dh-unibe/image-text_kurrent-xix/resolve/refs%2Fconvert%2Fparquet/default/train/"
fs = fsspec.filesystem("https")
f = fs.open(BASE + "0005.parquet")
pf = pq.ParquetFile(f)
t = pf.read_row_group(5)
os.makedirs(W + "/test", exist_ok=True)
names = t.column("filename").to_pylist()
xmls = t.column("xml_content").to_pylist()
imgs = t.column("image").to_pylist()
for n, x, im in zip(names, xmls, imgs):
    stem = n.rsplit(".", 1)[0]
    open(os.path.join(W, "test", stem + ".xml"), "w").write(x)
    b = im["bytes"] if isinstance(im, dict) else im
    open(os.path.join(W, "test", n), "wb").write(b)
print("test pages:", len(names), flush=True)

def gt_lines(xml_path):
    tree = etree.parse(xml_path)
    lines = []
    for tl in tree.iter():
        if etree.QName(tl).localname != 'TextLine':
            continue
        pts = None
        for ch in tl:
            if etree.QName(ch).localname == 'Coords':
                pts = ch.get('points'); break
        if not pts:
            continue
        xy = []
        for p in pts.strip().split():
            a, b = p.split(','); xy.append((float(a), float(b)))
        xs = [p[0] for p in xy]; ys = [p[1] for p in xy]
        if max(xs) - min(xs) < 5 or max(ys) - min(ys) < 3:
            continue
        lines.append([min(xs), min(ys), max(xs), max(ys)])
    return lines

def iou(a, b):
    x0, y0 = max(a[0], b[0]), max(a[1], b[1])
    x1, y1 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, x1 - x0) * max(0, y1 - y0)
    ua = (a[2]-a[0])*(a[3]-a[1]) + (b[2]-b[0])*(b[3]-b[1]) - inter
    return inter / ua if ua > 0 else 0

tg = tp = trh = tph = 0
per_page = {}
t0 = time.time()
for n in names:
    stem = n.rsplit(".", 1)[0]
    im = Image.open(os.path.join(W, "test", n)).convert("RGB")
    gt = gt_lines(os.path.join(W, "test", stem + ".xml"))
    seg = blla.segment(im, model=seg_model, device="cpu")
    pred = []
    for l in seg.lines:
        pts = l.boundary if getattr(l, "boundary", None) else l.baseline
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        pred.append([min(xs), min(ys), max(xs), max(ys)])
    used = set(); rh = 0
    for g in gt:
        bst, bj = 0, -1
        for j, p in enumerate(pred):
            v = iou(g, p)
            if v > bst:
                bst, bj = v, j
        if bst >= 0.5:
            rh += 1; used.add(bj)
    tg += len(gt); tp += len(pred); trh += rh; tph += len(used)
    per_page[stem] = {"gt": len(gt), "pred": len(pred), "rec_hits": rh}
    print(f"page {stem} gt={len(gt)} pred={len(pred)} hits={rh} elapsed={round(time.time()-t0)}s", flush=True)

out = {"model": "segv2 best_0.6469 (8 projects x 150 pages, val MM_1_005, best epoch 13 val_mean_iu 0.6469)",
       "protocol": "bbox IoU>=0.5, same 29 MM_1_006 held-out pages as segv1",
       "gt": tg, "pred": tp,
       "recall": round(trh / tg, 4), "precision": round(tph / max(tp, 1), 4),
       "compare": {"base_blla": {"recall": 0.9018, "precision": 0.9597}, "segv1": {"recall": 0.9426, "precision": 0.9835}},
       "per_page": per_page}
json.dump(out, open(W + "/segv2_eval_results.json", "w"), indent=1)
print("SEGV2 EVAL " + json.dumps({k: v for k, v in out.items() if k != "per_page"}), flush=True)
print("DONE", flush=True)
