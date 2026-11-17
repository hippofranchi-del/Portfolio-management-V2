"""Figure 5. The fund against the security market line, at its own beta.
Inputs as in Table 3 (see risk_model.py)."""
from decimal import ROUND_HALF_UP, Decimal

import matplotlib.pyplot as plt

from common import BLUE, INK, ORANGE, save
from risk_model import RF, RM, table3

table, _ = table3()
base, live = table["Fund: base case"], table["Fund: live-record case"]
B, req = base["beta"], base["required"]
print(f"beta {B:.2f}, required {req:.2f}%, base {base['expected']:.2f}% (alpha {base['alpha']:+.2f}%), "
      f"live {live['expected']:.2f}% (alpha {live['alpha']:+.2f}%)")

fig, ax = plt.subplots(figsize=(5.6, 4.2))
ax.plot([0, 1.4], [RF, RF + 1.4 * (RM - RF)], color="#555555", lw=2.0, zorder=1)
ax.text(0.30, RF + 0.30 * (RM - RF) - 0.95, "Security market line", rotation=20, color="#555555", fontsize=10)
ax.plot(0, RF, "o", color="#555555", ms=8, zorder=3)
ax.text(0.03, RF - 0.75, f"Risk-free {RF:.1f}%", fontsize=9.5, color="#555555")
ax.plot(1, RM, "o", color="#333333", ms=11, zorder=3)
ax.text(1.0, RM - 0.9, f"S&P 500\nβ = 1.00, {RM:.1f}%", fontsize=10, color=INK, ha="center", va="top")
ax.annotate("", xy=(B, base["expected"] - 0.12), xytext=(B, req + 0.06),
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.0))
ax.plot(B, base["expected"], "o", color=BLUE, ms=12, zorder=3)
base_label = Decimal(str(round(base["expected"], 6))).quantize(Decimal("0.1"), ROUND_HALF_UP)  # 10.95 -> 11.0
ax.text(B - 0.04, base["expected"] + 0.4, f"Quality fund, base case\nβ = {B:.2f}, {base_label}%",
        fontsize=10, fontweight="bold", color=INK, ha="right", va="bottom")
ax.text(B - 0.05, 9.85, f"α = {base['alpha']:+.1f}%", fontsize=11, fontweight="bold", color=INK,
        ha="right", va="center")
ax.plot(B, live["expected"], "o", mfc="white", mec=BLUE, mew=2, ms=10, zorder=3)
ax.text(B + 0.05, live["expected"] - 0.25,
        f"Live-record case\n{live['expected']:.2f}%, α = " + f"{live['alpha']:.2f}%".replace("-", "−"),
        fontsize=9.5, color=INK, va="top")
ax.set_xlim(0, 1.45)
ax.set_ylim(3, 12.8)
ax.set_xlabel("Beta")
ax.set_ylabel("Expected 12-month return (%)")
ax.set_title(f"At its own beta of {B:.2f}, the fund still sits\nabove the security market line",
             loc="left", fontweight="bold", fontsize=12.5, pad=10)
save(fig, "fig5_security_market_line.png", size=(1124, 846))
