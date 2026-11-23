# Stock Portfolio Dashboard

One dashboard for a five-stock portfolio, built from **real market prices**
downloaded from Yahoo Finance — nothing here is simulated or invented.

Tickers: **AAPL, MSFT, NVDA, GOOGL, AMZN**, from 2023-01-01 to 2026-11-23
(change them with `--tickers`, `--start`, `--end`).

## What it computes

- **Growth of $1** invested in each stock and in an equal-weighted portfolio
- **Daily-return distributions** for each stock
- **Rolling 30-day volatility** (annualised)
- **Drawdowns** — how far each holding fell from its peak, and the worst one
- **Correlation heatmap** of daily returns
- **Risk vs return** — annualised return against annualised volatility,
  plus the **Sharpe ratio** (risk-free rate assumed 4%)

## How to run

```bash
pip install -r requirements.txt
python portfolio_dashboard.py
python portfolio_dashboard.py --tickers AAPL MSFT NVDA --start 2024-01-01
```

## Output

- `dashboard.png` — the six-panel dashboard figure
- `metrics.csv` — annualised return, volatility, Sharpe ratio, max drawdown,
  and total return per ticker (and for the portfolio)
- `prices.csv` — the downloaded adjusted closing prices

If a ticker fails to download (a network hiccup), the script retries once,
warns, and builds the dashboard from the tickers that did come through.
