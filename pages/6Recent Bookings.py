# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="100 most recent Accom Bookings",layout="wide")

st.title("100 most recent Accom Bookings")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

df = pd.read_csv("../../Downloads/Bookings Clean.csv")

df["Created"] = pd.to_datetime(df["Created"])
# df["Created"] = df["Created"] + pd.DateOffset(hours=9) ALREADY MOVED TO CLEAN BOOKINGS



df['Start date'] = pd.to_datetime(df['Start date'])
df['Start date'] = df['Start date'].dt.strftime('%d-%m-%Y')

# df = df[df.Created>pd.to_datetime('2023-01-01')]


df = df[["Created","ID","Season","Lead Guest","ChannelAS1","Gross","Net","Vendor","Product","Start date","Nights"]]



payments_data = pd.read_csv("../../Downloads/Payments Clean.csv")

payments_data = payments_data[["Booking ID","Invoice ID","Paid","Invoice Type","Due Date"]]


payment_1_paid_df = payments_data[(payments_data["Invoice Type"]=="Payment - 1")]
payment_2_paid_df = payments_data[(payments_data["Invoice Type"]=="Payment - 2")]


df = pd.merge(df,payment_1_paid_df['Paid'], left_on =df['ID'],right_on=payment_1_paid_df["Booking ID"], how = 'left')
df = df.rename(columns={'Paid': 'Invoice 1'})
df = df.drop("key_0",axis=1)
df["Invoice 1"] = np.where(df["Invoice 1"].isnull(),"No Invoice",df["Invoice 1"])
df["Invoice 1"] = np.where(df["Invoice 1"]=="1.0","Paid",df["Invoice 1"])
df["Invoice 1"] = np.where(df["Invoice 1"]=="0.0","Not Paid",df["Invoice 1"])


df = pd.merge(df,payment_2_paid_df['Paid'], left_on =df['ID'],right_on=payment_2_paid_df["Booking ID"], how = 'left')
df = df.rename(columns={'Paid': 'Invoice 2'})
df = df.drop("key_0",axis=1)
df["Invoice 2"] = np.where(df["Invoice 2"].isnull(),"No Invoice",df["Invoice 2"])
df["Invoice 2"] = np.where(df["Invoice 2"]=="1.0","Paid",df["Invoice 2"])
df["Invoice 2"] = np.where(df["Invoice 2"]=="0.0","Not Paid",df["Invoice 2"])


df["Invoice 1"] = np.where(df["ChannelAS1"]=="OTA","OTA",df["Invoice 1"])
df["Invoice 2"] = np.where(df["ChannelAS1"]=="OTA","OTA",df["Invoice 2"])

df["Invoice 1"] = np.where((df["Net"]==0)&(df["Gross"]==0),"Zero Stay",df["Invoice 1"])
df["Invoice 2"] = np.where((df["Net"]==0)&(df["Gross"]==0),"Zero Stay",df["Invoice 2"])

df = df[df.duplicated()==False]




def color_coding(row):
    return ['background-color:coral'] * len(
        row) if (row["Invoice 1"] == "Not Paid") else ['background-color:azure'] * len(row)

df = df.sort_values(by="Created")
df.Gross = df.Gross.apply(lambda x: round(x, 0))


# Set to keep it manageable
df = df[df.Season=="'23/24'"]

df["ID"]= df["ID"].astype(str)
# df.Gross = df.Gross.apply(lambda x: round(x, 0))
df.Gross = df.Gross.astype(int).round(1)
df.Net = df.Net.astype(int).round(1)

df = df.tail(100)
st.dataframe(df.style.apply(color_coding, axis=1),1400,600)




# st.table(df)
# st.dataframe(df.tail(15),1300,600)