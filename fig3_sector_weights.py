"""Figure 3. Sector weights of the fund against the S&P 500.

S&P 500 sector weights are each stock's share of total float market
capitalisation, a proxy for the official index weights.
"""
import numpy as np
import matplotlib.pyplot as plt

from common import BLUE, GREY, MUTED, load_workbook_data, save, title

universe, portfolio, _ = load_workbook_data()

sectors = {}  # sector -> [S&P 500 weight %, fund weight %]
for u in universe:
    if u["bench"]:
        sectors.setdefault(u["sector"], [0.0, 0.0])[0] += u["bench"] * 100
for p in portfolio:
    sectors.setdefault(p["sector"], [0.0, 0.0])[1] += p["weight"] * 100
order = sorted(sectors, key=lambda k: sectors[k][1] - sectors[k][0])
for k in order[::-1]:
    print(f"{k:28s} fund {sectors[k][1]:5.1f}%  S&P 500 {sectors[k][0]:5.1f}%")

fig, ax = plt.subplots(figsize=(6.3, 4.6))
yy = np.arange(len(order))
h = 0.38
ax.barh(yy + h / 2 + 0.01, [sectors[k][1] for k in order], height=h, color=BLUE, label="Portfolio", linewidth=0)
ax.barh(yy - h / 2 - 0.01, [sectors[k][0] for k in order], height=h, color=GREY, label="S&P 500", linewidth=0)
for i, k in enumerate(order):
    active = sectors[k][1] - sectors[k][0]
    ax.text(max(sectors[k]) + 0.7, i, f"{active:+.1f}".replace("-", "−"), va="center", fontsize=10, color=MUTED)
ax.set_yticks(yy)
ax.set_yticklabels(order, fontsize=11)
ax.tick_params(axis="y", length=0)
ax.set_xlabel("Weight (%); labels show portfolio minus S&P 500")
ax.set_xlim(0, 41)
ax.xaxis.grid(True, color="#E6E6E6", linewidth=0.8)
ax.set_axisbelow(True)
ax.legend(frameon=False, loc="lower right", fontsize=10.5)
title(ax, "Overweight Financials and Industrials;\nno Utilities or Real Estate", x=-0.52)
save(fig, "fig3_sector_weights.png")
