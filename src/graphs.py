import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def price_chart(close_prices, ma_short, ma_long, short_days, long_days):
    
    fig = plt.figure(figsize=(12, 10))
    
    close_prices = close_prices.copy()
    close_prices.index = pd.to_datetime(close_prices.index)
    
    plt.plot(close_prices.index, close_prices.values, label="Close Price")
    plt.plot(ma_short.index, ma_short.values, label=f"MA ({short_days})")
    plt.plot(ma_long.index, ma_long.values, label=f"MA ({long_days})")

    log_prices = np.log(close_prices.values)
    days = np.arange(len(log_prices))

    avg_days = days.mean()
    avg_log = log_prices.mean()

    if (((days - avg_days) ** 2).sum()) != 0:
        slope = (((days - avg_days) * (log_prices - avg_log)).sum()) / (((days - avg_days) ** 2).sum())
        y_intercept = avg_log - slope * avg_days
        trend_line = np.exp(slope * days + y_intercept)

        plt.plot(close_prices.index, trend_line, label="Trend Line", linestyle="--")
    
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(7))
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(loc='best')
    plt.grid(True)

    return fig


def rsi_chart(rsi_values):

    fig = plt.figure(figsize=(12, 10))
    
    rsi_values = rsi_values.copy()
    rsi_values.index = pd.to_datetime(rsi_values.index)
    
    plt.plot(rsi_values.index, rsi_values.values)
    plt.title("Relative Strength Index (RSI)")
    plt.axhline(70, linestyle="--")
    plt.axhline(30, linestyle="--")
    plt.ylim(0, 100)
    
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(6))
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.xlabel("Date")
    plt.ylabel("RSI")
    plt.legend(loc='best')
    plt.grid(True)

    return fig
