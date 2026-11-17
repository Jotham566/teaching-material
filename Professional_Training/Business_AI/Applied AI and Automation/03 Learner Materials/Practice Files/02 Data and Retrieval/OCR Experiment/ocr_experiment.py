"""Reproducible OCR experiment for Sessions 5 and 11.

Reads passages.txt (one passage per block, blocks separated by a blank line),
renders each passage under three printing conditions, runs Tesseract, and
writes results.csv and summary.txt.

Requires: Python 3, Pillow, numpy and the tesseract command line tool
(language pack eng). Nothing is downloaded. The renderings are synthetic
approximations of a clean print-out and of photocopies; they are not scans
from a firm's archive.

Conditions (fixed in this file so a rerun gives comparable results):
  A  clean      200 dpi, 11 pt serif, black on white
  B  mild       100 dpi equivalent, 9 pt, 1.2 degree skew, light blur, noise
  C  moderate   85 dpi equivalent, 8 pt, 1.5 degree skew, blur, noise, reduced contrast
  D  severe     75 dpi equivalent, 8 pt, 2.0 degree skew, heavier blur, noise, low contrast
The ladder was fixed before the final run and every condition is reported,
including conditions where Tesseract returns unusable text.
Usage: python3 ocr_experiment.py [passages.txt] [output_folder]
"""
import sys, csv, re, subprocess, random, shutil, platform
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
PASSAGES = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "passages.txt"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "ocr_output"
FONTS = ["/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
         "/Library/Fonts/Times New Roman.ttf", "/System/Library/Fonts/Supplemental/Times New Roman.ttf"]
FONT = next((f for f in FONTS if Path(f).exists()), None)
CONDITIONS = {
    "A_clean":     dict(dpi=200, pt=11, skew=0.0, blur=0.0, noise=0.0,  contrast=1.0),
    "B_mild":      dict(dpi=100, pt=9,  skew=1.2, blur=0.6, noise=10.0, contrast=0.9),
    "C_moderate":  dict(dpi=85,  pt=8,  skew=1.5, blur=0.7, noise=12.0, contrast=0.85),
    "D_severe":    dict(dpi=75,  pt=8,  skew=2.0, blur=0.9, noise=18.0, contrast=0.75),
}

def wrap(draw, text, font, width):
    lines, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if draw.textlength(t, font=font) <= width: line = t
        else: lines.append(line); line = w
    lines.append(line)
    return lines

def render(text, cond, seed):
    c = CONDITIONS[cond]
    scale = 200 / c["dpi"]                      # draw at 200 dpi then degrade resolution
    size = int(c["pt"] * 200 / 72)
    font = ImageFont.truetype(FONT, size)
    W = 1500
    probe = ImageDraw.Draw(Image.new("L", (W, 10), 255))
    lines = wrap(probe, text, font, W - 160)
    H = 120 + int(len(lines) * size * 1.35) + 80
    img = Image.new("L", (W, H), 255); d = ImageDraw.Draw(img)
    y = 80
    for ln in lines:
        d.text((80, y), ln, font=font, fill=0); y += int(size * 1.35)
    rnd = np.random.default_rng(seed)
    if c["dpi"] != 200:
        small = img.resize((int(W / scale), int(H / scale)), Image.BILINEAR)
        img = small.resize((W, H), Image.BILINEAR)
    if c["blur"]: img = img.filter(ImageFilter.GaussianBlur(c["blur"]))
    if c["skew"]: img = img.rotate(c["skew"], resample=Image.BICUBIC, expand=True, fillcolor=255)
    a = np.asarray(img).astype(float)
    a = 255 - (255 - a) * c["contrast"]
    if c["noise"]: a = a + rnd.normal(0, c["noise"], a.shape)
    return Image.fromarray(np.clip(a, 0, 255).astype("uint8"))

def ocr(path):
    r = subprocess.run(["tesseract", str(path), "stdout", "-l", "eng", "--psm", "6"], capture_output=True, text=True)
    return " ".join(r.stdout.split())

def words(s): return re.findall(r"[A-Za-z0-9’'\-\.]+", s.lower())

def edit(a, b):
    n, m = len(a), len(b); prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        prev = cur
    return prev[m]

NEG = re.compile(r"\b(not|no|never|neither|nor|without|except|unless|cannot|shall not|may not)\b", re.I)

def main():
    if not FONT: sys.exit("No serif font found; edit FONTS.")
    blocks = [b.strip().replace("\n", " ") for b in PASSAGES.read_text(encoding="utf-8").split("\n\n") if b.strip()]
    OUT.mkdir(exist_ok=True, parents=True)
    rows = []
    for i, p in enumerate(blocks, 1):
        ref = words(p); negs = [m.group(0).lower() for m in NEG.finditer(p)]
        for cond in CONDITIONS:
            f = OUT / f"p{i:02d}_{cond}.png"
            render(p, cond, seed=1000 + i).save(f)
            got = ocr(f); gw = words(got)
            err = edit(ref, gw); acc = max(0.0, 1 - err / max(1, len(ref)))
            kept = sum(1 for n in negs if re.search(r"\b" + re.escape(n) + r"\b", got, re.I))
            rows.append(dict(passage=i, condition=cond, ref_words=len(ref), word_errors=err,
                             word_accuracy=round(acc, 3), negations_in_source=len(negs), negations_kept=kept,
                             changed_meaning_flag="CHECK" if kept < len(negs) else "", ocr_text=got))
    with (OUT / "results.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    v = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
    ver = (v.stdout or v.stderr).splitlines()[0]
    lines = [f"OCR experiment: {ver}, language eng, psm 6; {platform.platform()}",
             f"Passages: {len(blocks)}. Conditions fixed in ocr_experiment.py. Synthetic renderings, not a firm's archive.", ""]
    for cond in CONDITIONS:
        rs = [r for r in rows if r["condition"] == cond]
        tw = sum(r["ref_words"] for r in rs); te = sum(r["word_errors"] for r in rs)
        tn = sum(r["negations_in_source"] for r in rs); tk = sum(r["negations_kept"] for r in rs)
        bad = sum(1 for r in rs if r["changed_meaning_flag"])
        unusable = sum(1 for r in rs if r["word_accuracy"] < 0.5)
        mean_acc = sum(r["word_accuracy"] for r in rs) / len(rs)
        lines.append(f"{cond}: mean word accuracy {mean_acc:.1%}; passages below 50% accuracy (unusable) {unusable} of {len(rs)}; negation words kept {tk} of {tn}; passages with at least one negation word missing from the output {bad} of {len(rs)}")
    (OUT / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
main()
