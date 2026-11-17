"""Figure 2. Distribution of quality z-scores: the 100 holdings against the
other eligible stocks, with the selection cut-off."""
import numpy as np
import matplotlib.pyplot as plt

from common import BLUE, GREY, INK, load_workbook_data, save

universe, _, _ = load_workbook_data()

eligible = [u for u in universe if u["eligible"]]
z_sel = np.array([u["qz"] for u in eligible if u["selected"]])
z_not = np.array([u["qz"] for u in eligible if not u["selected"]])
cut = z_sel.min()
print(f"selected {len(z_sel)}, not selected {len(z_not)}, cut-off {cut:.2f}")

fig, ax = plt.subplots(figsize=(5.6, 4.2))
bins = np.arange(-1.9, 2.11, 0.1)
ax.hist([z_not, z_sel], bins=bins, stacked=True, color=[GREY, BLUE], edgecolor="white", linewidth=0.8,
        label=[f"Not selected ({len(z_not)})", f"Selected ({len(z_sel)})"])
ax.axvline(cut, color=INK, ls="--", lw=1.1)
ax.text(cut + 0.04, ax.get_ylim()[1] * 0.93, f"Cut-off: {cut:.2f}", fontsize=10.5, color="#555555", va="top")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], frameon=False, fontsize=10.5, loc="upper left")
ax.set_xlabel("Quality z-score (average of the ROE, leverage and accruals z-scores)", fontsize=10.5)
ax.set_ylabel("Number of stocks", fontsize=11)
ax.set_title(f"The {len(z_sel)} holdings are the top of the quality\n"
             f"distribution of {len(eligible)} eligible stocks",
             loc="left", fontweight="bold", fontsize=12.5)
save(fig, "fig2_quality_score_distribution.png", size=(1108, 846))
