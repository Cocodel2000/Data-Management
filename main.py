import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plotplotly
from plotly import graph_objs as go

START = "2010-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("stock prediction app")

stocks = ("APPL","GOOGL","MSFT")
selected_stocks = st.selectbox("Select dataset for preditcion", stocks)

n_years = st.slider ("Years of prediction:", 1, 5)
period = n_years * 365

@st.cache
def load_data(ticker):
    data = yfinance.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Load data ...")
data = load_data(selected_stocks)
data_load_state.text("Load data ... done!")

st.subheader("Raw data")
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["Date"], y =date["Ajd Close"], name="stock"))
    fig.layout.update(title_text="Time series data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

#forecasting

df_train = data[["Date", "Ajd Close"]]
df_train = df_train.rename(columns={"Date": "ds", "Ajd Close": "y"})

m= Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periodes=period)
forecast = m.predict(future)

st.subhearder("Forecast data")
st.write(forecast.tail())

st.write("forecast data")
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)
