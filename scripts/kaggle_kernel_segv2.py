# kurrent-segv2: seg round 2 - fine-tune kraken blla on 8 diverse MM projects x 150 pages
# (MM_1_001/002/003/004/007/008/009/010). Public-domain data only (HF dh-unibe/image-text_kurrent-xix).
# MM_1_005 = val only (first 120 pages, never trained). MM_1_006 fully held out (test only, row group 5
# of file 0005 = the exact 29 segv1 test pages, same IoU protocol -> direct comparison to segv1 recall 0.9426).
# Target: recall > 0.97. Fixes segv1's BEST-glob bug (recursive glob catches <out>/best_*.safetensors).
# Authorization: overnight mandate phonemsg-01M7639R7189XFHFSYR9V7E50R (user, 2026-11-11 22:02).
import subprocess, sys, os, json, time, glob

def sh(cmd):
    print("+", cmd, flush=True)
    r = subprocess.run(cmd, shell=True)
    if r.returncode != 0:
        raise RuntimeError("failed: " + cmd)

# 1. deps (torch/torchvision preinstalled on Kaggle GPU image; kraken --no-deps to avoid CUDA wheel pull)
sh("pip install -q --no-deps kraken==7.1.1")
sh("pip install -q lightning htrmopo cattrs shapely scikit-image pyarrow jsonschema lxml python-bidi coremltools fsspec requests safetensors iso639-lang scikit-learn scipy threadpoolctl \"click<8.3\"")

from kraken import blla
from kraken.lib import vgsl
import pyarrow.parquet as pq
import fsspec
print("imports OK", flush=True)

W = "/kaggle/working"
# 2. base model
sh("curl -sL -o {}/blla.mlmodel https://zenodo.org/api/records/22879549/files/blla.mlmodel/content".format(W))

# 3. stage pages from HF parquet (HTTP range reads)
BASE = "https://huggingface.co/datasets/dh-unibe/image-text_kurrent-xix/resolve/refs%2Fconvert%2Fparquet/default/train/"
fs = fsspec.filesystem("https")

def fetch_rows(file_idx, row_groups=None, max_rows=None):
    url = BASE + f"{file_idx:04d}.parquet"
    f = fs.open(url)
    pf = pq.ParquetFile(f)
    tables = []
    rgs = row_groups if row_groups is not None else range(pf.metadata.num_row_groups)
    for rg in rgs:
        tables.append(pf.read_row_group(rg))
    import pyarrow as pa
    t = pa.concat_tables(tables)
    if max_rows and t.num_rows > max_rows:
        t = t.slice(0, max_rows)
    return t

def dump(t, outdir):
    os.makedirs(outdir, exist_ok=True)
    names = t.column("filename").to_pylist()
    xmls = t.column("xml_content").to_pylist()
    imgs = t.column("image").to_pylist()
    for n, x, im in zip(names, xmls, imgs):
        stem = n.rsplit(".", 1)[0]
        open(os.path.join(outdir, stem + ".xml"), "w").write(x)
        b = im["bytes"] if isinstance(im, dict) else im
        open(os.path.join(outdir, n), "wb").write(b)
    print("dumped", len(names), "->", outdir, flush=True)
    return names

t0 = time.time()
# train: 8 diverse projects x 150 pages each (files 0,1,2,3,6,7,8,9 = MM_1_001..004, 007..010)
import pyarrow as pa
_parts = []
for fi in (0, 1, 2, 3, 6, 7, 8, 9):
    _t = fetch_rows(fi, max_rows=150)
    _proj = "MM_1_%03d" % (fi + 1)
    print("train part", _proj, _t.num_rows, "pages", flush=True)
    _parts.append(_t)
tr = pa.concat_tables(_parts)
assert tr.num_rows == 8 * 150, f"train pages {tr.num_rows}"
train_names = dump(tr, W + "/seg/train")
# val: MM_1_005 (file 0004), first 120 pages
va = fetch_rows(4, max_rows=120)
val_names = dump(va, W + "/seg/val")
# test: MM_1_006 file 0005 row group 5 (the exact 29 baseline pages)
te = fetch_rows(5, row_groups=[5])
test_names = dump(te, W + "/seg/test")
print("staging sec", round(time.time() - t0, 1), flush=True)

def wlist(names, outdir, path):
    with open(path, "w") as fh:
        for n in names:
            fh.write(os.path.join(outdir, n.rsplit(".", 1)[0] + ".xml") + "\n")

wlist(train_names, W + "/seg/train", W + "/train.txt")
wlist(val_names, W + "/seg/val", W + "/val.txt")
wlist(test_names, W + "/seg/test", W + "/test.txt")

# 4. fine-tune
sh("ketos -d cuda:0 segtrain -f page -i {W}/blla.mlmodel --resize union --augment "
   "-q early -N 50 --min-epochs 5 --lag 8 -F 1 -t {W}/train.txt -e {W}/val.txt -o {W}/segv2".format(W=W))

best = sorted(glob.glob(W + "/segv2/**/best_*.safetensors", recursive=True))
if not best:
    best = sorted(glob.glob(W + "/segv2*best*"))
if not best:
    best = sorted(glob.glob(W + "/segv2/**/*.safetensors", recursive=True) + glob.glob(W + "/segv2/**/*.mlmodel", recursive=True))
assert best, "no segv2 checkpoint found"
BEST = best[-1]
print("BEST:", BEST, flush=True)

# 5. segtest (baseline-detection metrics)
sh("ketos -d cuda:0 segtest -m {}/blla.mlmodel -f page -e {}/test.txt".format(W, W))
sh("ketos -d cuda:0 segtest -m {} -f page -e {}/test.txt".format(BEST, W))

# 6. IoU protocol (same as local baseline): recall/precision at bbox IoU>=0.5 on the 29 test pages
from lxml import etree
from PIL import Image

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
    x0 = max(a[0], b[0]); y0 = max(a[1], b[1]); x1 = min(a[2], b[2]); y1 = min(a[3], b[3])
    inter = max(0, x1 - x0) * max(0, y1 - y0)
    ua = (a[2]-a[0])*(a[3]-a[1]) + (b[2]-b[0])*(b[3]-b[1]) - inter
    return inter / ua if ua > 0 else 0

def iou_eval(model_path):
    model = vgsl.TorchVGSLModel.load_model(model_path)
    if not getattr(model, "user_metadata", None) or "hyper_params" not in model.user_metadata:
        if not getattr(model, "user_metadata", None):
            model.user_metadata = {}
        model.user_metadata["hyper_params"] = {}
    tg = tp = trh = tph = 0
    for n in test_names:
        stem = n.rsplit(".", 1)[0]
        im = Image.open(os.path.join(W, "seg/test", n)).convert("RGB")
        gt = gt_lines(os.path.join(W, "seg/test", stem + ".xml"))
        seg = blla.segment(im, model=model, device="cuda:0")
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
    return {"gt": tg, "pred": tp, "recall": round(trh / tg, 4), "precision": round(tph / max(tp, 1), 4)}

before = iou_eval(W + "/blla.mlmodel")
after = iou_eval(BEST)
metrics = {"model": BEST, "baseline": before, "finetuned": after,
           "train_pages": len(train_names), "val_pages": len(val_names), "test_pages": len(test_names)}
json.dump(metrics, open(W + "/segv2_metrics.json", "w"), indent=2)
print("METRICS " + json.dumps(metrics), flush=True)
print("DONE", flush=True)
