#!/usr/bin/env python3
"""news-image-01 entry (Python 3.13, standard library only).

The image is entry.png beside this file: a one-page editorial infographic
summing up Friday 13 November 2026 in six verified stories, drawn by
gen_image.py. This program copies it to /output/entry.png, byte for byte,
so both graded runs write identical bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SRC = os.path.join(HERE, "entry.png")
DST = os.path.join(OUT, "entry.png")

if not os.path.isfile(SRC):
    sys.exit("entry.png missing beside main.py")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, DST)
# Both graded runs must write the same bytes: confirm the copy is whole.
if os.path.getsize(SRC) != os.path.getsize(DST):
    sys.exit("copy incomplete: size mismatch")
print("wrote", DST, os.path.getsize(DST), "bytes")
sys.exit(0)
