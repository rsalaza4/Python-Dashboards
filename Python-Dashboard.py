# Import required libraries
import yfinance as yf
import pandas as pd
import hvplot.pandas
import panel as pn
pn.extension('plotly')
import plotly.express as px
import plotly.graph_objects as go

# Get stock data
TSLA_data = yf.Ticker("TSLA").history(period='1d', start='2020-1-1', end='2021-10-29')

# Visualize data frame top rows
TSLA_data.head()

# Select 'Close' column only
TSLA = TSLA_data[["Close"]].copy()

# Add a daily return column
TSLA["Daily_Return"] = TSLA["Close"].pct_change()

# Add a simple moving average column of window of 10 days
TSLA["SMA10"] = TSLA["Close"].rolling(window=10).mean()

# Add a simple moving average column of window of 50 days
TSLA["SMA50"] = TSLA["Close"].rolling(window=50).mean()

# Add a simple moving average column of window of 100 days
TSLA["SMA100"] = TSLA["Close"].rolling(window=100).mean()

# Visualize data frame top rows
TSLA.head()

# Create an hvplot table for the stock data
TSLA_df_table = TSLA.hvplot.table(width=1000)

# Create an hvplot line plot for the closing price
TSLA_closing_price_plot = TSLA.drop(columns="Daily_Return").hvplot.line(title="TSLA Closing Price & Simple Moving Average", ylabel="USD", height=500, width=1000)

# Create an hvplot line plot for the daily return
TSLA_daily_retrun_plot = TSLA["Daily_Return"].hvplot.line(title="TSLA Daily Returns", ylabel="Daily Return", height=500, width=1000)

# Create an hvplot bar plot for the daily volume
TSLA_trading_volume_barplot = TSLA_data["Volume"].hvplot.bar(title="TSLA Trading Volume", ylabel="Volume", height=500, width=1000).opts(alpha=0.2, xaxis=None)

# Create a candlestick plot for the stock data
TSLA_candlestick = go.Figure(data=[go.Candlestick(x=TSLA_data.index,
                    open=TSLA_data['Open'],
                    high=TSLA_data['High'],
                    low=TSLA_data['Low'],
                    close=TSLA_data['Close'])])
TSLA_candlestick.update_layout(height=800, width=1000, title='TSLA Candlestick')

# Create a title for the dashboard
title = pn.pane.Markdown(
    """
# Tesla Stock Analysis Dashboard
""",
width=1000,
)

# Create a welcome message for the dashboard
welcome = pn.pane.Markdown(
    """
This dashboard presents a visual analysis of Telsa stock (ticker: "TSLA") from January 2020 to October 2021.
You can navigate through the tabs below and interact with the plots to explore more details about the Tesla stock.
"""
)

# Define the ditinct tabs for the dashboard with their corresponding plots
tabs = pn.Tabs(
    ("Historical Data", pn.Column(TSLA_df_table)),
    ("Candlestick Plot", pn.Column(TSLA_candlestick)),
    ("Closing Price and Volume", pn.Column(TSLA_closing_price_plot, TSLA_trading_volume_barplot)),
    ("Daily Returns", pn.Column(TSLA_daily_retrun_plot)),
)

# Build dashboard
dashboard = pn.Column(pn.Column(title, welcome), tabs, width=1000)

# Visualize dashboard
dashboard.servable()
