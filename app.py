import streamlit as st
from datetime import date, datetime, timedelta
import pandas as pd

from src.data import price_data
from src.key_metrics import (
    total_return,
    annualized_volatility,
    max_drawdown,
    moving_average,
    rsi
)
from src.trends import regression_trend, type_of_trend, momentum_signal
from src.graphs import price_chart, rsi_chart

st.set_page_config(page_title="Equity Trend Analyzer", layout="wide")

st.title("📈 Equity Trend Analyzer")
st.caption("In this project I've created, it analyzes price trends and basic risk metrics using historical market data (yfinance API).")

with st.sidebar:
    st.header("Please enter the necessary inputs:")

    ticker = st.text_input("Ticker", value="AAPL").strip().upper()

    end_default = date.today()
    start_default = end_default - timedelta(days=365)

    start_date = st.date_input("Start Date", value=start_default)
    end_date = st.date_input("End Date", value=end_default)

    interval = st.selectbox("Interval", ["1d", "1h"], index=0)

    short_days = st.number_input("Short MA (days)", min_value=5, max_value=200, value=20, step=5)
    long_days = st.number_input("Long MA (days)", min_value=10, max_value=300, value=50, step=10)

    st.divider()

    rsi_button = st.checkbox("Show RSI", value=True)
    run = st.button("Analyze The Equity!")

if short_days >= long_days:
    st.warning("Short MA period should be less than Long MA period.")
    st.stop()
    
if not run:
    st.info("Please enter inputs on the left and click **Analyze The Equity!**.")
    st.stop()

if ticker == "":
    st.error("Please enter a valid ticker symbol.")
    st.stop()

if start_date >= end_date:
    st.error("Dates are invalid - Start date must be before end date.")
    st.stop()

with st.spinner("Downloading the price data..."):
    df = price_data(ticker, start_date, end_date, interval)

if df is None or df.empty:
    st.error("No data found for the given ticker and date range. Please check the inputs.")
    st.stop()

if "Close" not in df.columns:
    st.error("No 'Close' price data available for the given ticker.")
    st.stop()

idx = pd.to_datetime(df.index, errors="coerce")
last_dt = idx.max()

if pd.isna(last_dt):
    st.caption("Last updated: **N/A**")
else:
    if last_dt.hour == 0 and last_dt.minute == 0 and last_dt.second == 0:
        st.caption(f"Last updated: **{last_dt.strftime('%Y-%m-%d')}**")
    else:
        st.caption(f"Last updated: **{last_dt.strftime('%Y-%m-%d %H:%M')}**")

close_prices = df["Close"].squeeze().dropna()

initial_price = close_prices.iloc[0]
buy_hold_returns = close_prices / initial_price - 1

returns = close_prices.pct_change().dropna()

total_returns = total_return(close_prices)
volatility = annualized_volatility(returns, interval)

mdd, _ = max_drawdown(close_prices)

slope, r_squared = regression_trend(close_prices)
trend_label = type_of_trend(slope, r_squared)

ma_short = moving_average(close_prices, int(short_days))
ma_long = moving_average(close_prices, int(long_days))
ma_signal = momentum_signal(ma_short, ma_long, int(short_days), int(long_days))
    
rsi_values = rsi(close_prices) if rsi_button else None

#streamlit layout and styling
st.markdown("""<style>.pill {display: inline-block; padding: 10px 18px; border-radius: 999px;
            font-size: 16px; font-weight: 600; margin-right: 8px; margin-bottom: 8px; white-space: nowrap;
            border: 1px solid #e5e7eb; background: #f8fafc;}
            .green-box { background: #ecfdf5; border-color: #a7f3d0; color: #065f46; }
            .red-box { background: #fef2f2; border-color: #fecaca; color: #7f1d1d; }
            .gray-box { background: #f3f4f6; border-color: #e5e7eb; color: #374151; }
            .kpi-row div[data-testid="stMetric"]{background: white; border: 1px solid #e5e7eb; 
            border-radius: 14px; padding: 12px;} </style>""", unsafe_allow_html=True)

st.markdown("""<style>.row-formatting {display: flex; flex-wrap: nowrap; gap: 12px; align-items: center;
            margin-bottom: 12px; overflow-x: auto;} </style> """, unsafe_allow_html=True)

tr_card, av_card, mdd_card, bh_card, ts_card = st.columns(5)
tr_card.metric("Total Return:", f"{total_returns*100:.2f}%")
av_card.metric("Annual Volatility:", f"{volatility*100:.2f}%")
mdd_card.metric("Max Drawdown:", f"{mdd*100:.2f}%")
ts_card.metric("Trend Strength ($R^2$):", f"{r_squared:.2f}")
bh_card.metric("Buy & Hold Return:", f"{buy_hold_returns.iloc[-1] * 100:.2f}%")
st.write("")

trend_class = "gray-box"

if trend_label == "Uptrend":
    trend_class = "green-box"
elif trend_label == "Downtrend":
    trend_class = "red-box"

signal_class = "gray-box"
signal_lower = str(ma_signal).lower()

if "above" in signal_lower:
    signal_class = "green-box"
elif "below" in signal_lower:
    signal_class = "red-box"
    
boxes = (f"""<div class="row-formatting">
<span class="pill {trend_class}">Trend: {trend_label}</span>
<span class="pill {signal_class}">MA Signal: {ma_signal}</span>
""")

if rsi_button and rsi_values is not None and not rsi_values.dropna().empty:
    
    current_rsi = float(rsi_values.dropna().iloc[-1])

    rsi_class = "gray-box"
    
    if current_rsi >= 70:
        rsi_class = "red-box"
    elif current_rsi <= 30:
        rsi_class = "green-box"
        
    boxes += (f'<span class="pill {rsi_class}">RSI (14): {current_rsi:.1f}</span>')

boxes += "</div>"

st.markdown(boxes, unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns([1.5, 1])

with col1:
    
    st.subheader("Price Trend Analysis 📊: ")
    st.pyplot(price_chart(close_prices, ma_short, ma_long, int(short_days), int(long_days)))
    
    if rsi_button and rsi_values is not None and not rsi_values.dropna().empty:
        st.subheader("RSI Graph (Period: 14)")
        st.pyplot(rsi_chart(rsi_values.dropna()))
    else:
        if rsi_button:
            st.info("Not enough data points to compute RSI.")

with col2:
    st.subheader("Notes 📝: ")
    st.write(f"**Ticker:** {ticker}")
    st.write(f"**Interval:** {interval}")
    st.write(f"**Date Range:** {start_date} -> {end_date}")
    st.write(f"**Regression Slope:** {slope:.4f}")

st.divider()

st.subheader("Raw Data 📋:")

if len(df) <= 30:
    raw_data_df = df
else:
    first_15 = df.head(15)
    last_15 = df.tail(15)
    break_row = pd.DataFrame([["..."] * len(df.columns)], columns=df.columns)
    break_row.index = ["..."]
    raw_data_df = pd.concat([first_15, break_row, last_15])

st.dataframe(raw_data_df, use_container_width=True)

st.divider()

csv_download = df.to_csv(index=True).encode("utf-8")
st.download_button(label="Download Data As CSV 📥", data=csv_download, file_name=f"{ticker}_Data_{start_date}_to_{end_date}.csv", mime="text/csv", use_container_width=True)
    