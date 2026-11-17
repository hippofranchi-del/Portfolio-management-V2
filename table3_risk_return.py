"""Table 3. Expected 12-month risk and return of the fund against the S&P 500.

Prints the table and writes it to table3_risk_return.csv.
"""
import csv

from common import OUTPUT
from risk_model import table3

table, info = table3()
print(f"Fund beta {info['beta_raw']:.4f} (holdings with a beta: {info['coverage']:.1f}% of the fund); "
      f"residual risk {info['sigma_e']:.2f}%")

ROWS = [("Expected return", "expected", "{:.2f}%"), ("Assumed excess return", "excess", "{:.2f}%"),
        ("Beta", "beta", "{:.2f}"), ("Volatility", "vol", "{:.2f}%"),
        ("Required return (CAPM)", "required", "{:.2f}%"), ("Jensen's alpha", "alpha", "{:.2f}%"),
        ("Sharpe ratio", "sharpe", "{:.2f}"), ("Treynor ratio", "treynor", "{:.2f}%"),
        ("Tracking error", "te", "{:.2f}%"), ("Information ratio", "ir", "{:.2f}")]
cols = list(table)

with open(OUTPUT / "table3_risk_return.csv", "w", newline="") as f:
    out = csv.writer(f)
    out.writerow(["Measure"] + cols)
    print(f"\n{'Measure':24s}" + "".join(f"{c:>24s}" for c in cols))
    for label, key, fmt in ROWS:
        cells = ["n/a" if table[c][key] is None else fmt.format(table[c][key]).replace("-", "−") for c in cols]
        out.writerow([label] + cells)
        print(f"{label:24s}" + "".join(f"{v:>24s}" for v in cells))
print("\nsaved table3_risk_return.csv")
