"""Inputs and calculations behind Table 3 and Figure 5 (Section 6).

Expected 12-month risk and return of the fund against a passive S&P 500
holding, using the CAPM and the single-index model (Bodie, Kane and Marcus).
"""
import csv
import math

from common import BETAS

# ---- Inputs (sources as in the Table 3 note of the essay)
RF = 3.9            # risk-free rate, %: midpoint of the Fed's 3.75-4.00% target range (Section 2)
RM = 8.1            # expected S&P 500 return, %: 5.1% ten-year Treasury yield + assumed 3% equity risk premium
SIGMA_M = 15.6      # S&P 500 volatility, %: Ung, Luk and Kang (2014), Exhibit 11
PAPER_BETA = 0.83   # S&P 500 Quality Index beta: Exhibit 11
PAPER_TE = 5.5      # S&P 500 Quality Index tracking error, %: Exhibit 11
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


def table3():
    beta_raw, coverage = fund_beta()
    beta = round(beta_raw, 2)  # the essay uses the beta rounded to two decimals
    # Residual (non-market) risk implied by the paper: TE^2 = ((1 - beta)^2 * sm^2) + se^2
    sigma_e = math.sqrt(PAPER_TE ** 2 - ((1 - PAPER_BETA) * SIGMA_M) ** 2)
    sigma_p = math.sqrt((beta * SIGMA_M) ** 2 + sigma_e ** 2)          # fund volatility
    te = math.sqrt(((beta - 1) * SIGMA_M) ** 2 + sigma_e ** 2)         # tracking error vs S&P 500
    required = RF + beta * (RM - RF)                                   # CAPM required return

    table = {"S&P 500": dict(expected=RM, excess=None, beta=1.0, vol=SIGMA_M, required=RM,
                             alpha=0.0, sharpe=(RM - RF) / SIGMA_M, treynor=RM - RF, te=0.0, ir=None)}
    for case, ex in EXCESS.items():
        er = RM + ex
        table[case] = dict(expected=er, excess=ex, beta=beta, vol=sigma_p, required=required,
                           alpha=er - required,                  # Jensen's (1968) alpha
                           sharpe=(er - RF) / sigma_p,
                           treynor=(er - RF) / beta,
                           te=te, ir=ex / te)                    # information ratio
    info = dict(beta_raw=beta_raw, coverage=coverage, sigma_e=sigma_e)
    return table, info
