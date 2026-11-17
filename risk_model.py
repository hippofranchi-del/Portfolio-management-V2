"""Inputs and calculations behind Table 4 and Figure 3 of the essay (Section 6).

Expected 12-month risk and return of the fund against a passive S&P 500
holding, using the CAPM (Jensen's alpha) and the Sharpe, Treynor and
information ratios.
"""
import csv

from common import BETAS

# ---- Inputs (sources as in the Table 4 note of the essay)
RF = 3.9            # risk-free rate, %: midpoint of the Fed's 3.75-4.00% target range (Section 2)
RM = 8.1            # expected S&P 500 return, %: 5.1% ten-year Treasury yield + assumed 3% equity risk premium (Section 2)

# Risk measured from Bloomberg: 104 weekly price returns over the two years to 16 November 2026,
# for the S&P 500 and for the current 100 holdings at today's portfolio weights.
SIGMA_M = 14.79     # S&P 500 volatility, % a year
SIGMA_P = 18.75     # fund volatility, % a year
TE = 7.18           # tracking error of the fund against the S&P 500, % a year
# Price rather than total returns: dividends are small and similar for the fund and the index,
# so using total returns would change these figures only marginally.

EXCESS = {          # assumed excess return over the S&P 500, %
    "Fund: base case": 2.85,          # index's long-run record, back-test plus live (Valantasis, 2026)
    "Fund: live-record case": 0.35,   # live record since the July 2014 launch (lower bound)
}


def fund_beta(path=BETAS):
    """Weighted Bloomberg adjusted beta (EQY_BETA) of the holdings that have one."""
    num = den = 0.0
    with open(path) as f:
        for row in csv.DictReader(f):
            if row["beta"]:
                w = float(row["weight_pct"])
                num += w * float(row["beta"])
                den += w
    return num / den, den


def table4():
    beta_raw, coverage = fund_beta()
    beta = round(beta_raw, 2)  # the essay uses the beta rounded to two decimals
    required = RF + beta * (RM - RF)                                   # CAPM required return

    table = {"S&P 500": dict(expected=RM, excess=None, beta=1.0, vol=SIGMA_M, required=RM,
                             alpha=0.0, sharpe=(RM - RF) / SIGMA_M, treynor=RM - RF, te=None, ir=None)}
    for case, ex in EXCESS.items():
        er = RM + ex
        table[case] = dict(expected=er, excess=ex, beta=beta, vol=SIGMA_P, required=required,
                           alpha=er - required,                  # Jensen's (1968) alpha
                           sharpe=(er - RF) / SIGMA_P,
                           treynor=(er - RF) / beta,
                           te=TE, ir=ex / TE)                    # information ratio
    info = dict(beta_raw=beta_raw, coverage=coverage)
    return table, info


table3 = table4  # older name, kept so existing scripts still run
