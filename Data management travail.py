#!/usr/bin/env python
# coding: utf-8

# In[6]:


pip install plotly_express==0.4.0


# In[7]:


pip install stocknews


# In[12]:


pip install streamlit


# In[2]:


pip install yfinance


# In[1]:


import streamlit as st, pandas as pd, numpy as np, yfinance as yf, plotly.express as px


# In[17]:


st.title("Stock Dashboard")


# In[ ]:


ticker = st.sidebar.text_input("Ticker")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.text_input("End Date")


# In[34]:


data =yf.download(ticker,start=start_date,end=end_date)
fig = px.line(data, x=data.index, y=data["Adj Close"], title=ticker)
st.plotly_chart(fig)


# In[20]:


pricing_data, fundamental_data, news = st.tabs(["Pricing Data","Fundamental Data","Top 10 News"])

with pricing_data:
    st.header("Price Movements")
    data2 = data
    data2["% Change"] = data["Adj Close"]/data["Adj Close"].shift(1) - 1
    st.write(data2)
    annual_return = data2["% Change"].mean()*252*100
    st.write("Annual Return is",annual_return,"%")
    stdev = np.std(data2["% Change"])*np.sqrt(252)
    st.write("Standard devation is",stdev*100,"%")
    st.write("Risk Ajd. Return is",annual_return/(stdev*100))
    


# In[26]:


pip install alpha_vantage


# In[28]:


from alpha_vantage.fundamentaldata import FundamentalData
key = "5O2RB0NXONEEN12V"
fd = FundamentalData(key, output_format="pandas")
with fundamental_data:
    fd = FundamentalData(key,output_format ="pandas")
    st.subheader("Balance Sheet")
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader("Income Statement")
    income_statement = fd.get_income_statement_annual(ticker)[0]
    is1= income_statement.T[2:]
    is1.columns = list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader("Cash Flow Statement")
    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)


# In[33]:


from stocknews import StockNews
with news:
    st.header(f"News of {ticker}")
    sn = StockNews(ticker,save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f"News {i+1}")
        st.write(df_news["published"][i])
        st.write(df_news["title"][i])
        st.write(df_news["summary"][i])
       


# In[ ]:




