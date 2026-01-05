# Equity Trend Analyzer 📈

This project is a simple **Streamlit** web app that analyzes an equity’s price action using **real historical market data (yfinance API)**. It calculates key risk/return metrics, determines the trend direction using linear regression, shows MA (moving average) signals, and optionally displays **RSI (14)** — all in a one-page dashboard with a CSV download.

---

## Features

- Downloads historical price data for a ticker (daily or hourly)
- Computes core metrics:
  - **Total Return**
  - **Annualized Volatility**
  - **Maximum Drawdown**
- Detects trends:
  - **Linear regression** -> returns **slope** and **R² (trend strength)**
  - Labels trend as **Uptrend / Downtrend / No Clear Trend**
- Momentum signal:
  - Compares **Short MA vs Long MA**
- Optional indicator:
  - **RSI (14)** with 70/30 reference levels
- Displays:
  - Price chart + MAs + trendline, with notes
  - RSI chart (optional)
  - Raw data preview
- Export:
  - **Download CSV** of the full dataset

---

## Tech Stack

- **Python**
- **Streamlit**
- **yfinance**
- **pandas**
- **NumPy**
- **Matplotlib**

---

## Project Structure

```text
equity-trend-analyzer/
│
├── app.py
├── requirements.txt
│
└── src/
    ├── data.py
    ├── key_metrics.py
    ├── trends.py
    └── graphs.py
```
