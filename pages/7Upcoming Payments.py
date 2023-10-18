# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from datetime import date
import datetime

st.set_page_config(page_title="Upcoming Payments",layout="wide")

st.title("Upcoming Payments")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

df = pd.read_csv("../../Downloads/Payments Clean.csv")

df["Created"] = pd.to_datetime(df["Created"])
df["Due Date"] = pd.to_datetime(df["Due Date"])

df["Paid"] = 0
paid_flag = df["Payment Date"].isnull()==False
df["Paid"] = np.where(paid_flag,1,df["Paid"])

df = df[df["Booking Status"]=="Active"]

df = df[["Booking ID","Invoice ID","Due Date","Lead Guest","Created By","Invoice Date",
"Invoice Amount","Payment Date","Payment Amount","Payment Method",
"Payment ID","Notes","1st Vendor","Product","Package Start Date","Package End Date","Booking Status","Booking Source","Segment","Season","7 Day Flag","Paid","Invoice Type"]]



def color_coding(row):
    return ['background-color:#ffb668'] * len(
        row) if (row["Paid"]==0) else ['background-color:azure'] * len(row)


df = df.sort_values(by="Due Date")
# df.Gross = df.Gross.apply(lambda x: round(x, 0))


        # today = date.today()

today = date.today()
df = df[df["Due Date"].dt.date > (today - datetime.timedelta(days=7))]
df = df[df["Due Date"].dt.date < (today + datetime.timedelta(days=7))]
df["Booking ID"] = df["Booking ID"].astype(str)

# # Set to keep it manageable
# df = df[df.Season=="'23/24'"]

# df["ID"]= df["ID"].astype(str)
# # df.Gross = df.Gross.apply(lambda x: round(x, 0))
# df.Gross = df.Gross.astype(int).round(1)
# df.Net = df.Net.astype(int).round(1)

# df = df.tail(100)
st.dataframe(df.style.apply(color_coding, axis=1),1400,600)




# st.table(df)
# st.dataframe(df.tail(15),1300,600)