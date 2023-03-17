import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries
from stocknews import StockNews

key = "5O2RB0NXONEEN12V"

st.title("Stock Dashboard")

ticker = st.sidebar.text_input("Ticker")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

data = yf.download(ticker, start=start_date_str, end=end_date_str)

fig = px.line(data, x=data.index, y="Adj Close", title=ticker)
st.plotly_chart(fig)

pricing_data, beta_data, dividend_data, fundamental_data, news = st.columns(5)
pricing_data, beta_data, dividend_data, fundamental_data, news = st.tabs(["Pricing Data","Beta Data","Dividend Data","Fundamental Data","Top 10 News"])

with pricing_data:
    st.header("Price Movements")
    data2 = data
    data2["% Change"] = data["Adj Close"] / data["Adj Close"].shift(1) - 1
    st.write(data2)
    annual_return = data2["% Change"].mean()*252*100
    st.write("Annual Return is",annual_return,"%")
    stdev = np.std(data2["% Change"])*np.sqrt(252)
    st.write("Standard devation is",stdev*100,"%")
    st.write("Risk Ajd. Return is",annual_return/(stdev*100))

with beta_data:
    st.header("Beta Data")
    beta = yf.Ticker(ticker).info["beta"]
    st.write(f"Beta: {beta}")

with dividend_data:
    st.header("Dividend Data")
    dividend_info = yf.Ticker(ticker).dividends
    if dividend_info.empty:
        st.write("This stock does not pay any dividends.")
    else:
        st.write(dividend_info)

fd = FundamentalData(key)

with fundamental_data:
    try:
        balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    except ValueError as e:
        st.write("Error getting data from the API:", e)
    else:
        bs = balance_sheet.T[2:]
        bs.columns = list(balance_sheet.T.iloc[0])
        st.subheader("Balance Sheet")
        st.write(bs)

        income_statement = fd.get_income_statement_annual(ticker)[0]
        is1= income_statement.T[2:]
        is1.columns = list(income_statement.T.iloc[0])
        st.subheader("Income Statement")
        st.write(is1)

        cash_flow = fd.get_cash_flow_annual(ticker)[0]
        cf = cash_flow.T[2:]
        cf.columns = list(cash_flow.T.iloc[0])
        st.subheader("Cash Flow Statement")
        st.write(cf)

with news:
    st.header(f"News of {ticker}")
    sn = StockNews(ticker,save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f"News {i+1}")
        st.write(df_news["published"][i])
        st.write(df_news["title"][i])
        st.write(df_news["summary"][i])



