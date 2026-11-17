# EC4430 Portfolio Management: quality portfolio (Sections 5 and 6)

This repository holds the code that produces the figures and the risk–return table in the Portfolio Builder sections (5 and 6) of our EC4430 group essay, University of St Andrews, November 2026.

The fund follows the quality strategy of Ung, Luk and Kang (2014). It ranks the S&P 500 on three ratios: return on equity, the balance-sheet accruals ratio and financial leverage. Each ratio is winsorised at the 2.5th and 97.5th percentiles and turned into a z-score. The three z-scores are averaged into one quality z-score, and the fund holds the top 20% of the index on that score (100 stocks). Each holding is weighted by quality score × float market capitalisation, with caps of 5% per stock and 40% per sector. The portfolio itself was built in Excel with Bloomberg data downloaded on 16 November 2026, and these scripts read that workbook.

## What each script produces

| Essay exhibit | Script | Output | Data used |
|---|---|---|---|
| Figure 1. Selection funnel | `src/fig1_selection_funnel.py` | `figures/fig1_selection_funnel.png` | Workbook, sheet *Scoring* |
| Figure 2. Distribution of quality z-scores | `src/fig2_quality_score_distribution.py` | `figures/fig2_quality_score_distribution.png` | Workbook, sheet *Scoring* |
| Figure 3. Sector weights against the S&P 500 | `src/fig3_sector_weights.py` | `figures/fig3_sector_weights.png` | Workbook, sheets *Scoring* and *Portfolio* |
| Figure 4. Quality and valuation against the S&P 500 | `src/fig4_quality_profile.py` | `figures/fig4_quality_profile.png` | Workbook, sheets *Scoring*, *Portfolio* and *Data* |
| Table 3. Expected risk and return | `src/table3_risk_return.py` | `output/table3_risk_return.csv` | `data/betas_bloomberg.csv` and inputs in `src/risk_model.py` |
| Figure 5. Security market line | `src/fig5_security_market_line.py` | `figures/fig5_security_market_line.png` | As for Table 3 |

Figure and table numbers follow our Sections 5–6.

## How to run

You need Python 3.9 or later.

```bash
pip install -r requirements.txt
python make_all.py
```

`make_all.py` runs every script in order. Each one also runs on its own, for example `python src/fig2_quality_score_distribution.py`. The scripts print the numbers they plot, such as sector weights, the selection cut-off and the weighted ratios, so each one can be checked against the essay. The Bloomberg workbook must be in `data/` first (see `data/README.md`).

## Method notes

- **Index weights:** the S&P 500 weights are each stock's share of total float market capitalisation. This is a proxy for the official index weights.
- **Figure 4 bases:** the fund is weighted by portfolio weight and the S&P 500 by float market capitalisation. Return on equity, debt/equity and accruals are weighted averages of the winsorised ratios. Price/earnings is the weighted harmonic mean on trailing 12-month EPS.
- **Fund beta:** this is the portfolio-weighted Bloomberg adjusted beta (`EQY_BETA`, two years of weekly returns against the S&P 500). It covers the 98 holdings that have a beta, 99.3% of the fund. FedEx Freight and Fifth Third had none. The result, 1.12, is rounded to two decimals as in the essay.
- **Table 3 inputs** (`src/risk_model.py`):
  - The risk-free rate of 3.9% is the midpoint of the Federal Reserve's 3.75–4.00% target range.
  - The expected S&P 500 return of 8.1% is the 5.1% ten-year Treasury yield plus an assumed 3% equity risk premium.
  - S&P 500 volatility (15.6%), and the Quality Index's beta (0.83) and tracking error (5.5%), come from Ung, Luk and Kang (2014), Exhibit 11.
  - The excess returns are 2.85% (the index's long-run record) and 0.35% (its live record since 2014), both from Valantasis (2026).
- **Single-index model:** fund volatility and tracking error follow σp = √(β²σm² + σe²), as in Bodie, Kane and Marcus. The residual risk σe = 4.8% is implied by the Exhibit 11 tracking error and beta.

## References

- Bloomberg L.P. (2026) *Bloomberg Terminal* [Database]. Accessed 16 November 2026.
- Jensen, M.C. (1968) 'The performance of mutual funds in the period 1945–1964', *Journal of Finance*, 23(2), pp. 389–416.
- S&P Dow Jones Indices (n.d.) *S&P Quality Indices Methodology*.
- Ung, D., Luk, P. and Kang, X. (2014) *Quality: A Distinct Equity Factor?* S&P Dow Jones Indices. Available at: https://ssrn.com/abstract=2472391.
- Valantasis, G. (2026) 'S&P 500 Quality Index: Why outperformance is only half the story', *Indexology Blog*, S&P Dow Jones Indices, 30 July.
