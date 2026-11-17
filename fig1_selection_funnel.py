"""Figure 1. Selection funnel: from the S&P 500 to the 100 holdings."""
import numpy as np
import matplotlib.pyplot as plt

from common import BLUE, INK, load_workbook_data, save, title

universe, portfolio, _ = load_workbook_data()

companies = [u for u in universe if not u["duplicate"]]
steps = [
    ("S&P 500 index lines", len(universe)),
    ("One share class per company", len(companies)),
    ("Positive EPS, book value and equity", sum(u["eligible"] for u in universe)),
    ("Top 20% of the index by quality score", sum(u["selected"] for u in universe)),
]
print(steps)

fig, ax = plt.subplots(figsize=(8.6, 2.9))
y = np.arange(len(steps))[::-1]
for (label, n), yy, alpha in zip(steps, y, [0.35, 0.55, 0.75, 1.0]):
    ax.barh(yy, n, height=0.68, color=BLUE, alpha=alpha, linewidth=0)
    ax.text(n + 8, yy, f"{n}", va="center", fontsize=12,
            fontweight="bold" if label.startswith("Top") else "normal", color=INK)
ax.set_yticks(y)
ax.set_yticklabels([s[0] for s in steps], fontsize=11.5, color="#333333")
ax.tick_params(axis="y", length=0)
ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
ax.set_xlim(0, 560)
title(ax, "Every holding comes out of the same rule-based screen", x=-0.62)
save(fig, "fig1_selection_funnel.png")
