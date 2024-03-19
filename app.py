import requests
import pandas as pd
import io
import streamlit as st

df1 = requests.get('https://api.orcascan.com/sheets/f5xG1-gqdcueAPfe?datetimeformat=DD/MM/YYYY HH:mm:ss&timezone=+00:00').content
df2 = requests.get('https://api.orcascan.com/sheets/rt7SbnAGBhSmb7EU?datetimeformat=DD/MM/YYYY HH:mm:ss&timezone=+00:00:').content
df3 = pd.read_csv(io.StringIO(df1.decode('utf-8')))
df4 = pd.read_csv(io.StringIO(df2.decode('utf-8')))
df5 = pd.concat([df3,df4["Scan_out"]], axis=1)
df5["scan_qty"] = df5["Scan_in"] - df5["Scan_out"]
df5["indiv_qty"] = df5["scan_qty"]*df5["Multiplier"]
df6 = df5.groupby(["Name"])[["Bulk_or_Indiv", "indiv_qty"]].agg(bulkindiv = ("Bulk_or_Indiv", lambda x:"Indiv"), qty = ("indiv_qty", "sum"))

df7 = df6.rename(columns={'bulkindiv': 'Status', 'qty': 'Product Quantity'})

st.dataframe(df7, width=1000, height=600)

refresh_button = st.button("Refresh")
if refresh_button:
    st.experimental_rerun()
