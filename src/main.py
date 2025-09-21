#!/usr/bin/env python3
"""
main.py - Generate animated GIF of tide data.

- Reads CSV with columns: datetime,height_m
- Dark blue background
- White line progressively drawn
- Saves GIF to output/hkotide.gif
"""

import argparse, io
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

def build_frames(x, y, fps=24, duration=8, width=1200, height=600):
    total = int(fps*duration)
    step = max(1, len(x)//total)

    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    fig.patch.set_facecolor("#001a33")
    ax.set_facecolor("#001a33")

    ax.tick_params(colors="white")
    for sp in ax.spines.values():
        sp.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.xaxis.label.set_color("white")
    ax.title.set_color("white")

    ax.set_title("Hong Kong Tides (HHOT) — White Line")
    ax.set_xlabel("Time index")
    ax.set_ylabel("Height (m)")
    ax.set_xlim(0, len(x)-1)
    margin = max(0.2, 0.05*(y.max()-y.min()))
    ax.set_ylim(y.min()-margin, y.max()+margin)
    ax.grid(True, alpha=0.2, color="white")

    frames = []
    for f in range(total):
        i = min((f+1)*step, len(x)-1)

        for ln in list(ax.lines):
            ln.remove()
        for txt in list(ax.texts):
            txt.remove()

        if i > 1:
            _x, _y = x[:i], y[:i]
            ax.plot(_x, _y, color="white", linewidth=2.5)
            ax.plot([x[i-1]], [y[i-1]], marker="o", markersize=6,
                    markerfacecolor="white", markeredgecolor="white")
            ax.text(x[i-1], y[i-1], f"{y[i-1]:.2f} m",
                    color="white", fontsize=10, ha="left", va="bottom")

        buf = io.BytesIO()
        fig.savefig(buf, format="png", facecolor=fig.get_facecolor(), bbox_inches="tight")
        buf.seek(0)
        frames.append(Image.open(buf).convert("RGB"))

    plt.close(fig)
    return frames

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="data/hhot_subset.csv")
    ap.add_argument("--out", default="output/hkotide.gif")
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--duration", type=int, default=8)
    args = ap.parse_args()

    df = pd.read_csv(args.csv, parse_dates=["datetime"]).sort_values("datetime")
    x = np.arange(len(df))
    y = df["height_m"].values

    frames = build_frames(x, y, fps=args.fps, duration=args.duration)

    # Ensure the output directory exists
    out_path = Path(args.out)
    if not out_path.parent.exists():
        out_path.parent.mkdir(parents=True, exist_ok=True)

    frames[0].save(args.out, save_all=True, append_images=frames[1:],
                   duration=int(1000/args.fps), loop=0)
    print(f"Saved GIF to {args.out}")

if __name__ == "__main__":
    main()