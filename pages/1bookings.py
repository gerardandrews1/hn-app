# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 17:31:22 2023

@author: andre
"""

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import datetime



st.set_page_config(page_title="HN Stuff",
                   page_icon=":bar_chart:",
                   layout="wide"
 )


df = pd.read_csv("../../Downloads/Bookings Clean.csv")

df["ID"] = df["ID"].astype(str)


df = df[["Created","ID","ChannelAS2","Custom ID","Gross","Nights","Start date","End date",
"Order Type","Vendor","Product","Email","Season",
"Option 1","Residency","Lead Guest", "Modified","Booking Source",
"Net","Notes","Agent Contact Name","Agent Contact Email","HN_Prop",
"Message","Long Stay","ChannelAS1","Zero Stay",	"Booking Month","Booking Year",
"Pre Season Nights","Early Dec Nights","Pre-Xmas Nights","Xmas/NY Nights","Powder 1 Nights",
"Lull Nights","Powder 2 Nights","CNY Nights","Late Feb Nights","Early March Nights",
"Late March Nights","Spring Skiing Nights"]]

# --------------- SIDE BAR -----------#
st.sidebar.header("Please filter here:")


channel = st.sidebar.multiselect(
    "Select the Channel:",
    options=["All","Direct","Agent","OTA","TBD"],
    default="All"
    )
if "All" in channel:
    channel = ["Direct","Agent","OTA","TBD"]


property_list = df["Vendor"].unique().tolist()
property_list.insert(0,"-All")


season = st.sidebar.multiselect(
    "Filter by Stay Season:",
    options=df["Season"].unique(),
    default="'23/24'")


vendor = st.sidebar.multiselect(
    "Filter by Property:",
    options=sorted(property_list, key=str.lower),
    default="-All"     
    )


if "-All" in vendor:
    vendor = df["Vendor"].unique().tolist()


hn_property = st.sidebar.multiselect(
    "For HN Props select 1 only",
    options=[1,0],
    default=[0,1]

)   


df_selection = df.query(
   "Vendor == @vendor & Season == @season & ChannelAS1 ==@channel & HN_Prop==@hn_property")


# ---------------Columns --------------#
df_selection_bookings = df_selection.shape[0]

sel_sum = df_selection.Gross.sum()


top_column1,top_column2,top_column3 = st.columns(3)


with top_column1:
    st.subheader(f"Bookings in selection: {df_selection_bookings} ")
    st.subheader(f"Gross of Selection: ¥{int(sel_sum):,} ")

# f"¥{agent_winter_gross:,}")


# -----------------Show df--------------#
st.dataframe(df_selection.sort_values(by="Created"))



# -------------Download button-------------#
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(df_selection)

st.download_button(
   "Press to Download",
   csv,
   "Your Download.csv",
   "text/csv",
   key='download-csv'
)
