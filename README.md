# Data

| File | Contents | Source |
|---|---|---|
| `SP500_Quality_Portfolio_Builder_v2.xlsx` | The portfolio workbook: raw fundamentals, the scoring of all S&P 500 members, and the 100 holdings with weights | Bloomberg Terminal, 16 November 2026 |
| `betas_bloomberg.csv` | Portfolio weight (%) and Bloomberg adjusted beta (`EQY_BETA`) for each holding. Blank means Bloomberg returned no beta | Bloomberg Terminal, 17 November 2026 |

## Workbook layout the scripts expect

- **Scoring:** headers on row 4 and one row per S&P 500 line from row 5. The scripts use these columns:
  - `Bloomberg ticker`, `Symbol`, `GICS sector`
  - `Duplicate share class?`, `Benchmark weight`
  - `ROE winsorised`, `Leverage winsorised`, `Accruals winsorised`
  - `Quality z (average)`, `Eligible?`, `Selected?`
- **Portfolio:** headers on row 10 and one row per holding from row 11. The scripts use `Symbol (MarketWatch)`, `GICS sector` and `Portfolio weight`.
- **Data:** the raw Bloomberg fields from row 5. Column A is the ticker, column D the last price (`PX_LAST`) and column G the trailing 12-month EPS.

To run the scripts on a workbook stored somewhere else, set the `EC4430_WORKBOOK` environment variable to its path.

**Licensing:** the workbook contains Bloomberg data, which Bloomberg's terms do not allow to be republished. Keep this repository private and share it only with the course staff.
