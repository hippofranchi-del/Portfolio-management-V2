"""Shared settings, chart style and data loading for the Sections 5-6 figures.

All portfolio data come from the Bloomberg workbook built for the essay
(see README.md). The workbook implements the quality screen of
Ung, Luk and Kang (2014) on the S&P 500, as of 16 November 2026.
"""
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from PIL import Image

# Every file sits in the repository's top folder: data, scripts and outputs.
ROOT = Path(__file__).resolve().parent
FIGURES = OUTPUT = ROOT
WORKBOOK = Path(os.environ.get("EC4430_WORKBOOK", ROOT / "SP500_Quality_Portfolio_Builder_v2.xlsx"))
BETAS = ROOT / "betas_bloomberg.csv"

# ---- Chart style (same for every figure in the essay)
BLUE, ORANGE, GREY, INK, MUTED = "#2B78D8", "#EC6A35", "#B8BEC6", "#1A1A1A", "#555555"
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": INK,
    "axes.linewidth": 1.0,
    "savefig.facecolor": "white",
})


def title(ax, text, x=0.0):
    ax.set_title(text, loc="left", fontweight="bold", fontsize=12.5, color="black", x=x, pad=10)


def save(fig, name, size=None):
    """Save at 200 dpi. If size=(w, h) is given, centre the chart on a white
    canvas of exactly that many pixels, the size of its frame in the essay."""
    path = FIGURES / name
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    if size:
        w, h = size
        im = Image.open(path).convert("RGB")
        W, H = im.size
        nw, nh = (W, round(W * h / w)) if W / H > w / h else (round(H * w / h), H)
        canvas = Image.new("RGB", (nw, nh), "white")
        canvas.paste(im, ((nw - W) // 2, (nh - H) // 2))
        canvas.resize((w, h), Image.LANCZOS).save(path)
    print("saved", path.relative_to(ROOT))


# ---- Data loading
def _num(v):
    if isinstance(v, bool):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _flag(v):
    return v in (True, 1, "True", "TRUE", "Yes", "YES")


def _table(ws, header_row):
    header = [c.value for c in ws[header_row]]
    rows = []
    for r in ws.iter_rows(min_row=header_row + 1, values_only=True):
        if r[0] is None:
            continue
        rows.append(dict(zip(header, r)))
    return rows


def load_workbook_data(path=WORKBOOK):
    """Return (universe, portfolio, prices) from the Bloomberg workbook.

    universe  - one dict per S&P 500 line (sheet 'Scoring', headers on row 4)
    portfolio - one dict per holding (sheet 'Portfolio', headers on row 10)
    prices    - {Bloomberg ticker: (price, trailing EPS)} (sheet 'Data', row 5 on)
    """
    if not Path(path).exists():
        raise FileNotFoundError(
            f"{path} not found. Put the Bloomberg workbook next to the scripts (see README.md).")
    wb = load_workbook(path, data_only=True)

    universe = []
    for s in _table(wb["Scoring"], 4):
        universe.append(dict(
            ticker=s["Bloomberg ticker"], symbol=s["Symbol"], sector=s["GICS sector"],
            duplicate=_flag(s["Duplicate share class?"]),
            bench=_num(s["Benchmark weight"]),
            roe=_num(s["ROE winsorised"]), lev=_num(s["Leverage winsorised"]),
            acc=_num(s["Accruals winsorised"]),
            qz=_num(s["Quality z (average)"]),
            eligible=_flag(s["Eligible?"]), selected=_flag(s["Selected?"]),
        ))

    portfolio = []
    for p in _table(wb["Portfolio"], 10):
        portfolio.append(dict(symbol=p["Symbol (MarketWatch)"], sector=p["GICS sector"],
                              weight=_num(p["Portfolio weight"])))

    # Sheet 'Data' holds the raw Bloomberg fields: column A ticker,
    # D last price (PX_LAST), G trailing 12-month EPS.
    prices = {}
    for r in wb["Data"].iter_rows(min_row=5, values_only=True):
        if r[0]:
            prices[r[0]] = (_num(r[3]), _num(r[6]))
    return universe, portfolio, prices
