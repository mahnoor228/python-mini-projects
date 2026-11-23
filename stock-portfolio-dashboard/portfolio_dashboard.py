"""
Stock portfolio dashboard — real market data, real risk numbers.

Downloads daily closing prices for five well-known stocks from Yahoo Finance
(via yfinance) and builds one dashboard from them:

  * growth of $1 invested in each stock (and in an equal-weighted portfolio)
  * daily-return distributions
  * rolling 30-day volatility
  * drawdowns (peak-to-trough losses) and each stock's worst drawdown
  * correlation heatmap of daily returns
  * risk vs return: annualised return against annualised volatility

All prices are REAL market data — nothing here is simulated or invented.
If a ticker fails to download (network hiccup), the dashboard is built from
the tickers that did come through and the failure is reported.

Run it:
    python portfolio_dashboard.py
    python portfolio_dashboard.py --tickers AAPL MSFT NVDA --start 2024-01-01

Outputs (in this folder):
    dashboard.png   — the six-panel dashboard figure
    metrics.csv     — annualised return, volatility, Sharpe, max drawdown, per ticker
    prices.csv      — the downloaded adjusted closing prices (cached real data)
"""

import argparse
import sys

import matplotlib

matplotlib.use("Agg")  # headless: save figures, don't try to open a window
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

DEFAULT_TICKERS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]
RISK_FREE_RATE = 0.04  # 4% — rough proxy for the US Treasury bill rate


def download_prices(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """Download adjusted closing prices. Retries once per ticker on failure."""
    prices = pd.DataFrame()
    for ticker in tickers:
        df = None
        for attempt in (1, 2):
            try:
                df = yf.download(ticker, start=start, end=end,
                                 auto_adjust=True, progress=False)
            except Exception as exc:  # noqa: BLE001 - network errors vary
                print(f"  {ticker}: download attempt {attempt} failed ({exc})")
                df = None
            if df is not None and not df.empty:
                break
        if df is None or df.empty:
            print(f"  WARNING: no data for {ticker}, skipping it.")
            continue
        prices[ticker] = df["Close"]
        print(f"  {ticker}: {len(df)} trading days, "
              f"{df.index[0].date()} to {df.index[-1].date()}")
    if prices.empty:
        sys.exit("ERROR: no price data downloaded for any ticker.")
    return prices.dropna()


def compute_metrics(prices: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame,
                                                   pd.DataFrame, pd.DataFrame]:
    """Returns, drawdowns, and a per-ticker risk/return summary."""
    returns = prices.pct_change().dropna()
    growth = (1 + returns).cumprod()  # growth of $1

    # Equal-weighted portfolio (rebalanced daily).
    weights = np.full(len(prices.columns), 1 / len(prices.columns))
    port_returns = returns @ weights
    returns["PORTFOLIO"] = port_returns
    growth["PORTFOLIO"] = (1 + port_returns).cumprod()

    # Drawdown: how far each series sits below its running peak.
    drawdown = growth / growth.cummax() - 1

    rows = []
    for name in returns.columns:
        r = returns[name]
        ann_return = r.mean() * 252
        ann_vol = r.std() * np.sqrt(252)
        sharpe = (ann_return - RISK_FREE_RATE) / ann_vol if ann_vol else np.nan
        rows.append({
            "ticker": name,
            "annualised_return": round(ann_return, 4),
            "annualised_volatility": round(ann_vol, 4),
            "sharpe_ratio": round(sharpe, 2),
            "max_drawdown": round(drawdown[name].min(), 4),
            "total_return": round(growth[name].iloc[-1] - 1, 4),
        })
    metrics = pd.DataFrame(rows).set_index("ticker")
    return returns, growth, drawdown, metrics


def plot_dashboard(returns, growth, drawdown, metrics, path: str) -> None:
    tickers = [c for c in growth.columns if c != "PORTFOLIO"]
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    fig.suptitle("Portfolio Dashboard — real prices from Yahoo Finance",
                 fontsize=15)

    # 1. Growth of $1.
    ax = axes[0, 0]
    for col in growth.columns:
        lw = 2.5 if col == "PORTFOLIO" else 1.4
        ls = "-" if col == "PORTFOLIO" else "-"
        ax.plot(growth.index, growth[col], label=col, lw=lw, ls=ls)
    ax.set_title("Growth of $1 invested")
    ax.set_ylabel("$")
    ax.legend(fontsize=8, ncol=3)
    ax.grid(alpha=0.3)

    # 2. Daily-return distributions.
    ax = axes[0, 1]
    ax.hist([returns[t] for t in tickers], bins=40, alpha=0.7,
            label=tickers, density=True)
    ax.set_title("Daily returns distribution")
    ax.set_xlabel("Daily return")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # 3. Rolling 30-day volatility.
    ax = axes[0, 2]
    for t in tickers:
        ax.plot(returns.index, returns[t].rolling(30).std() * np.sqrt(252),
                label=t, lw=1.2)
    ax.set_title("Rolling 30-day volatility (annualised)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # 4. Drawdowns.
    ax = axes[1, 0]
    for col in drawdown.columns:
        lw = 2.5 if col == "PORTFOLIO" else 1.2
        ax.plot(drawdown.index, drawdown[col] * 100, label=col, lw=lw)
    ax.set_title("Drawdown from peak (%)")
    ax.set_ylabel("%")
    ax.legend(fontsize=8, ncol=3)
    ax.grid(alpha=0.3)

    # 5. Correlation heatmap of daily returns.
    ax = axes[1, 1]
    corr = returns[tickers].corr()
    im = ax.imshow(corr.values, cmap="RdYlGn", vmin=-1, vmax=1)
    ax.set_xticks(range(len(tickers)))
    ax.set_yticks(range(len(tickers)))
    ax.set_xticklabels(tickers)
    ax.set_yticklabels(tickers)
    for i in range(len(tickers)):
        for j in range(len(tickers)):
            ax.text(j, i, f"{corr.values[i, j]:.2f}", ha="center",
                    va="center", fontsize=9)
    ax.set_title("Correlation of daily returns")
    fig.colorbar(im, ax=ax, shrink=0.8)

    # 6. Risk vs return.
    ax = axes[1, 2]
    # Small per-ticker nudges so nearby labels (GOOGL/AMZN) don't overlap.
    offsets = {"GOOGL": (-52, 6), "AMZN": (6, -14)}
    for name in metrics.index:
        ax.scatter(metrics.loc[name, "annualised_volatility"],
                   metrics.loc[name, "annualised_return"], s=90)
        dx, dy = offsets.get(name, (6, 4))
        ax.annotate(name, (metrics.loc[name, "annualised_volatility"],
                           metrics.loc[name, "annualised_return"]),
                    textcoords="offset points", xytext=(dx, dy), fontsize=9)
    ax.set_title("Risk vs return (annualised)")
    ax.set_xlabel("Volatility (std of daily returns × √252)")
    ax.set_ylabel("Mean daily return × 252")
    ax.grid(alpha=0.3)

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"Saved dashboard: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a stock portfolio dashboard.")
    parser.add_argument("--tickers", nargs="+", default=DEFAULT_TICKERS,
                        help="tickers to include (default: AAPL MSFT NVDA GOOGL AMZN)")
    parser.add_argument("--start", default="2023-01-01",
                        help="start date YYYY-MM-DD (default 2023-01-01)")
    parser.add_argument("--end", default="2026-11-23",
                        help="end date YYYY-MM-DD (default 2026-11-23)")
    args = parser.parse_args()

    print(f"Downloading {len(args.tickers)} tickers, {args.start} to {args.end}...")
    prices = download_prices(args.tickers, args.start, args.end)
    prices.to_csv("prices.csv")

    returns, growth, drawdown, metrics = compute_metrics(prices)
    metrics.to_csv("metrics.csv")

    print("\nSummary (annualised, 252 trading days/year):")
    print(metrics.to_string())
    print(f"\nBest Sharpe ratio: {metrics['sharpe_ratio'].idxmax()} "
          f"({metrics['sharpe_ratio'].max():.2f})")
    print(f"Worst max drawdown: {metrics['max_drawdown'].idxmin()} "
          f"({metrics['max_drawdown'].min():.1%})")

    plot_dashboard(returns, growth, drawdown, metrics, "dashboard.png")
    print("Done.")


if __name__ == "__main__":
    main()
