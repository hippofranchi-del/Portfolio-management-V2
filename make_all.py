"""Rebuild every figure and table for Sections 5-6 in one go:

    python make_all.py
"""
import runpy
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))

SCRIPTS = [
    "fig1_selection_funnel.py",
    "fig2_quality_score_distribution.py",
    "fig3_sector_weights.py",
    "fig4_quality_profile.py",
    "table3_risk_return.py",
    "fig5_security_market_line.py",
]

for name in SCRIPTS:
    print(f"\n=== {name}")
    runpy.run_path(str(SRC / name), run_name="__main__")
