"""Figure 4. Quality and valuation of the fund against the S&P 500.

Fund weighted by portfolio weight, S&P 500 by float market capitalisation.
Return on equity, debt/equity and accruals are weighted averages of the
winsorised ratios; price/earnings is the weighted harmonic mean on
trailing 12-month EPS.
"""
import matplotlib.pyplot as plt

from common import BLUE, GREY, INK, load_workbook_data, save

universe, portfolio, prices = load_workbook_data()
by_symbol = {u["symbol"]: u for u in universe}

fund_w = {p["symbol"]: p["weight"] for p in portfolio}
index_w = {u["symbol"]: u["bench"] for u in universe if not u["duplicate"] and u["bench"]}


def weighted_mean(weights, key):
    num = den = 0.0
    for sym, w in weights.items():
        v = by_symbol[sym][key]
        if v is None:
            continue
        num += w * v
        den += w
    return num / den


def harmonic_pe(weights):
    """Weighted harmonic mean P/E = sum(w) / sum(w * EPS / price)."""
    num = den = 0.0
    for sym, w in weights.items():
        price, eps = prices[by_symbol[sym]["ticker"]]
        if price is None or eps is None:
            continue
        num += w
        den += w * eps / price
    return num / den


stats = {
    "roe": (weighted_mean(fund_w, "roe"), weighted_mean(index_w, "roe")),
    "lev": (weighted_mean(fund_w, "lev"), weighted_mean(index_w, "lev")),
    "acc": (weighted_mean(fund_w, "acc"), weighted_mean(index_w, "acc")),
    "pe": (harmonic_pe(fund_w), harmonic_pe(index_w)),
}
for k, (f, i) in stats.items():
    print(f"{k:4s} fund {f:.3f}  S&P 500 {i:.3f}")

panels = [("Return on equity", "higher is better", stats["roe"], lambda v: f"{v * 100:.0f}%"),
          ("Debt / equity", "lower is better", stats["lev"], lambda v: f"{v:.2f}"),
          ("Accruals ratio", "lower is better", stats["acc"], lambda v: f"{v:.3f}"),
          ("Price / earnings", "lower is cheaper", stats["pe"], lambda v: f"{v:.1f}")]
fig, axes = plt.subplots(1, 4, figsize=(9.2, 3.4))
for ax, (label, note, vals, fmt) in zip(axes, panels):
    ax.bar([0, 1], vals, width=0.62, color=[BLUE, GREY], linewidth=0)
    for x, v in zip([0, 1], vals):
        ax.text(x, v + max(vals) * 0.03, fmt(v), ha="center", fontsize=11.5, color=INK)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Fund", "S&P 500"], fontsize=10.5)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_ylim(0, max(vals) * 1.22)
    ax.set_title(f"{label}\n({note})", fontsize=11, color="#333333", pad=6)
fig.suptitle("The fund is more profitable, lower in accruals and cheaper\nthan the index; its leverage is similar",
             x=0.05, ha="left", fontweight="bold", fontsize=12.5, y=1.13)
save(fig, "fig4_quality_profile.png", size=(1596, 774))
