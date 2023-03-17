import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries
from stocknews import StockNews
from pyChatGPT import ChatGPT

session_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..6OhxJHxRawld_Sv_.QcS-cVehRw-DGaVRt81It5_dXRgnAt5lMUquwUhiVn3lyCUAwaiTrvgdU4ZREcAE__B1c98oGOeGPQ9OSGfFRSDBFEo6NZQ2CNIb7qiD_qiv4dS1-6Bu6xGUvgwc1d7eJ-lK7CWBn1cVhdVs301B-gsxCSEZTZy25dNXrl77On9BM4HjFdaQgSFkWd4zkIxCG1wjSIC0FpeYtE6HqHfiRzsWWXBBvGdGEIda3ogoxMY37R7Z37EYQ0P5rooL97Skgokdu9IzXU9pgHvZtjRxo7lA58H_kgGQsAXtvqGWH7GepW6-lHnR7fQfCg_5wPgORYeHUgl7f3ZBVAFzAkQF0DXVfmE1RVo2Mgm2HpB_JcrnsmEChj5qsh4dbmhMYUqUWCvADW8VtFMavdfXBk2C7c2wVtOMR6QzPxi6cQQW4dhAnIUgHEZMBByKYpE16nxXi-AKWTOpwaKEf5UKXgoJcw8ycDS14tjfoXkFudbjeNnk-dW8ibssH2CSzhmW1PEigejEyf48n89VPiNp-bHS0-CEmXRGqEAEkLqbTWPI-Uw37lefGh8wJL2hJtZCt7l-NwwuvH0ik5htdGegyqLMTbs5E-3zWhqj02LWlQuK8vWw2F_C09V9DViBGZHMUJod1OD7uDB3ZsktZy0EYPYxvF7VESCMTosyodmCme95K7kz-2WqmTMwu5PNjnv0YZv6YIgCpfReO6Mf1Orud-oVd6KADne-stLLuKW7mhpGr-3V2QiloJqKQBLZpK3lzkrAD8RhPUu07QjmdWZbKdoll3l_8uUDH7U_7NJgo08vQAneP3Rg2qk7PtxgtcChLJMWo5t71pPj-MbzGfVyc0E-RvLLCUYi4d7rlHrwqDiCtp3fzq0kkJgCLNKBd5HhJ6HHg1OCe0_8EbULe85lbcWrZz6LnBN7yB-aQrZ_2tf6Bw4b423JCct-hu5jlZewTNogszqciPJEnGcfIf0PPuyc9yiLuZwwxqE45WD8uB47cK7Q1K6dLcsHaxsMKzFXHw-mXXOKXlRf4-US7xvflOGWN-uNt3yI_9PMUzJLV-QKQAgODTehO976MORPL4hWEYa3BmUTwCFcF-zya9QLgqY9c37fNNwcvKm4qKfzosotnamY8w7W6_FEYBHbN9Sr6ixhFLzcLuDubbAtHVBQOfdYanjd5jG8-XcotvYFVMCvQERU9VV0hxRzBYVmeuKFakmAsW700nuQvCqMFfLOq8lYIotCZA41ABLIUATAPVgGvTZHjCk8y9JL0c2m6IXCHrBCG4QvMEgUsKb0O6N1FGu30iQGIzxCjZZ17YekuEMYnsIchwsX29mn2ouHRLr0nVwNx1CUhbKvamPXijcY4VZZW9bBMPdW2B2J79OjM_m0uL69XeHxSDzNG37FXs4P5rYGHoUMf-QYD_epu90dVArGbIwgBxZaiBjN5WZVTXyFsHzpV1woPMXwkZNcaSCD6ado3Qp6m2ggtSmXuJ0KK2iX3eE5VUnIeZZycsGPRT3Hq_v3iqGrTiexe2BtKCRwcislrsDP_1KmcqSxn0Z7qiFr68mUv9rTWioJThDwgNQn_E8X-0YeiZyL5X2sAv9ub976_1ykUSmdYgeOxyaVRDQ0WcR4a1i4NQ2-8Jxo1p-KK70ioM6utUtU1w34GlW2ZAODshx6fUxj2xzDK4qnvqNP0NCetEUML4QXuhCTOJG7jlviXw8gD3pkF7HIT-RzK5prUtaulOWj7rdS7nq71Hrv9mqQxO630W_Bv8ziOxY0Xb4P9e6BnSXe4UxYu1BZGtXlQVF-1gN_-SToNAfksJCaasicNVOfgcQllq6QfDO0UueY4HWMvUhfpHROCT3izPCyhDSdXD8Z7F4zoq9aVwpGfAlkTEurpfkaNUPwQlqOLaowmKE5iGvz2_91EdRS6FW3Qwv-Dzl7FyZDAInpPZD9JwUAKytI41Mw5G1lnk7P9SWeqIkcsClVwfkNDReECmNMVi9cQyLn0aUiRAX9VKpLhUswM9RMocTBrizKmdBgVQXTWUbjm80J97VJAHv3-h7aaIOzUX3Lv3nCrIve77H9K_hofyysDbYc2fjXKIuMwu_BnjIwDajJG3zE34niJPJnXRVe7_Pv9BxNdFrvWNg9gJVtW5m3eoUY17wp2hAhSNwKxxw8JY_5RyRs3lWdGZaPd8KKmC_WssL9hyH7FL_m4Geqvq4FEgiGw5vdThm9XKddIgXSVmRUAf_HuMPWbpBlUJyVO53GND-XifvROje7Db_VrAXVlw1VRYVRf4rT1XL7d8ZTKczvMNBp5sw99Xn8IVnt3QTGixIql6X84CQwAbaj_CsuQ7lb1pxNsc8RVSGP8k0vRJK6oCENArvD0mfQFztZwhm0-rlhscmh34QICbgzliG13ZYg7uaVpDWk5JWL3ztTP9rPzUFZ9mWdH0uvrvMpKRRm3dqr1HLO2vV3VgF5uhQwYPxtF_2QGG_ETGL5UI0W4jywqyetEbkr-aNZog5ZNgmkgpLrC3d_NyltQrUqW0Uttsc44jBR10ENsTRFpiTtdpNwNgePohoyLk7JyNcHTEH3FlDmbDOU9j1sg4zcB_77rE1H3w.mBhwr2aihRZCQbNxmuOcMQ"
api2 = ChatGPT(session_token)

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

pricing_data, beta_data, dividend_data, fundamental_data, news, openai1 = st.columns(6)
pricing_data, beta_data, dividend_data, fundamental_data, news, openai1 = st.tabs(["Pricing Data","Beta Data","Dividend Data","Fundamental Data","Top 10 News","OpenAI ChatGPT"])

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
    stock_info = yf.Ticker(ticker).info
    beta = stock_info.get("beta")
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


buy = api2.send_message(f"3 Reasons to buy {ticker} stock")
sell = api2.send_message(f"3 Reasons to sell {ticker} stock")
swot = api2.send_message(f"SWOT analysis of {ticker} stock")

with openai1:
    buy_reason, sell_reason, swot_analysis = st.tabs(["3 Reasons to buy","3 Reasons to sell","SWOT analysis"])

    with buy_reason:
        st.subheader(f"3 Reasons to buy {ticker} stock")
        st.write(buy["message"])
    with sell_reason:
        st.subheader(f"3 Reasons to sell {ticker} stock")
        st.write(sell["message"])
    with swot_analysis:
        st.subheader(f"SWOT analysis of {ticker} stock")
        st.write(swot["message"])
