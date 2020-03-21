import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
sns.set(style="whitegrid")

# Title
# =========================================================================================

st.title('Cō Vidis?')

st.markdown('''
    **Cō Vidis?** [kʷoː ˈwɪːdɪs] ➡️ latin for "COVID-19, where are you going?"
    (https://en.wikipedia.org/wiki/Quo_vadis)

    A Dashboard to follow the state of the Coronavirus with a focus on Switzerland 🇨🇭.

    ---
''')

# Functions
# =========================================================================================

def create_by_country_dataframe(df):
    by_country = df.T
    by_country.columns = by_country.loc["Country/Region"]
    by_country = by_country[4:]
    by_country = by_country.groupby(axis=1, by=by_country.columns).sum()
    by_country.index = pd.to_datetime(by_country.index)
    return by_country

def is_it_spreading(df):
    return df.diff()


# Data Loading
# =========================================================================================

data = "../../data/raw/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/"

confirmed = f"{data}time_series_19-covid-Confirmed.csv"
deaths = f"{data}time_series_19-covid-Deaths.csv"
recovered = f"{data}time_series_19-covid-Recovered.csv"

df_confirmed = pd.read_csv(confirmed)
df_deaths = pd.read_csv(deaths)
df_recovered = pd.read_csv(recovered)

df = {
    "confirmed": df_confirmed,
    "deaths": df_deaths,
    "recovered": df_recovered
}


# Compute a Index by Country
# =========================================================================================

by_country = {
    "confirmed" : create_by_country_dataframe(df.get("confirmed")),
    "deaths" : create_by_country_dataframe(df.get("deaths")),
    "recovered" : create_by_country_dataframe(df.get("recovered"))
}

# Compute the existing cases and add them to the Dictionnary

# Active cases = total confirmed - total recovered - total deaths
by_country["existing"] = by_country["confirmed"] - by_country["recovered"] - by_country["deaths"]


# Regions of Interest
# =========================================================================================

CH = ["Switzerland"]
CH_neighbors = ["Italy", "France", "Liechtenstein", "Austria", "Germany"]
CH_neighbors_no_italy = ["France", "Liechtenstein", "Austria", "Germany"]

# Bulgaria, Cyprus and Romania are not in the list
# Switzerland has been added
EU = ["Switzerland","Austria","Belgium","Croatia","Denmark","Estonia","Finland","France","Germany","Greece","Hungary","Ireland","Italy","Latvia","Lithuania","Luxembourg","Malta","Netherlands","Poland","Portugal","Romania","Slovakia","Slovenia","Spain","Sweden"]
EU_no_italy = ["Switzerland","Austria","Belgium","Croatia","Denmark","Estonia","Finland","France","Germany","Greece","Hungary","Ireland","Latvia","Lithuania","Luxembourg","Malta","Netherlands","Poland","Portugal","Romania","Slovakia","Slovenia","Spain","Sweden"]


# Period of Interest
# =========================================================================================

last_n_days = 14

existing = by_country.get("existing")[-last_n_days:]
confirmed = by_country.get("confirmed")[-last_n_days:]
deaths = by_country.get("deaths")[-last_n_days:]
recovered = by_country.get("recovered")[-last_n_days:]


# Sidebar
# =========================================================================================

st.sidebar.markdown("""
    ## Data
    The data source is checked at 6:00, 12:00 and 18:00 GMT+1 (Swiss time).
    https://github.com/CSSEGISandData/COVID-19
""")
st.sidebar.markdown(f"last available data : {by_country['existing'].iloc[-1].name.date()}")

st.sidebar.markdown("""
    ## Author
    Fred Montet 
    https://twitter.com/fredmontet
    
    ## Repository
    https://github.com/fredmontet/co-vidis

    """)


st.markdown("## Switzerland")
# ========================================================================================= 

# Existing Cases
fig, ax = plt.subplots()
fig.tight_layout(pad=2)
ax = existing[CH].sum(axis=1).plot(title="Cases in Switzerland")
ax = deaths[CH].sum(axis=1).plot()
ax.legend(["Existing (log scale in dashed)", "Deaths"])
axlog = ax.twinx()
axlog = existing[CH].sum(axis=1).plot(ax=axlog, logy=True, style="--")
axlog.grid(False)
st.pyplot()

## Linear Regression from New Cases
df = existing[CH].diff()[1:]
X = df.index.factorize()[0].reshape(-1,1)
Y = df.values
m = LinearRegression().fit(X, Y)
Y_pred = m.predict(X)
Y_pred = pd.DataFrame(Y_pred)
Y_pred.index = df.index
Y_pred = Y_pred.rename(columns={0:"Trend"})

## Plot New Cases
fig, ax = plt.subplots()
fig.tight_layout(pad=2)
Y_pred.plot(ax=ax, style="--", title="New cases per day in Switzerland")
existing[CH].diff().plot(ax=ax, style=".", color="black", title="New cases per day in Switzerland")
ax.legend(["Trend", "New Cases"])
st.pyplot()


st.markdown("## Surrounding Countries")
# =========================================================================================

df1 = pd.DataFrame(by_country["existing"][CH_neighbors + CH].iloc[-1].astype(int))
df2 = pd.DataFrame(by_country["deaths"][CH_neighbors + CH].iloc[-1].astype(int))
df1.rename(columns={df1.columns[-1]:"Existing"}, inplace=True)
df2.rename(columns={df2.columns[-1]:"Deaths"}, inplace=True)
df = pd.concat([df1,df2], axis=1)

option = st.selectbox('Choose the type of cases', ('Existing', 'Deaths'))

fig, ax = plt.subplots()
ax.grid(True)
df.get(option).plot.bar(title=f"{option} Cases", color="slategray", ax=ax);
for p in ax.patches:
    ax.annotate(str(p.get_height()), 
                 (p.get_x()+p.get_width()/2., p.get_height()), 
                 ha='center', 
                 va='center', 
                 xytext=(0, 6),
                 textcoords='offset points',
                 fontweight="bold")
st.pyplot()


st.markdown("## Europe")
# =========================================================================================

df = by_country["existing"]

fig, ax = plt.subplots()
fig.tight_layout(pad=2)
df.sum(axis=1).plot(ax=ax, figsize=(7,6), title="Exisiting cases")
df[EU].sum(axis=1).plot(ax=ax)
df[CH_neighbors].sum(axis=1).plot(ax=ax)
df[CH].sum(axis=1).plot(ax=ax)
ax.legend(["Total", "Europe", "CH Neighbors", "CH"]);
st.pyplot()

# =========================================================================================
