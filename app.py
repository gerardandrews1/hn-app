# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import datetime
from datetime import date
import seaborn as sns
import time
import os
import sys

st.set_page_config(layout="wide")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

df = pd.read_csv("Bookings Clean.csv")

df["Created"] = pd.to_datetime(df["Created"])


df['Start date'] = pd.to_datetime(df['Start date'])
df['Start date'] = df['Start date'].dt.strftime('%d-%m-%Y')



df = df[["Created","ID","Lead Guest","ChannelAS1","ChannelAS2","Gross","Net","Vendor","Product","Start date","Nights","Booking Year","Booking Month","Season"]]



# SIDE BAR ACTION #
season_list = ["'23/24'", "'Summer 23'",
"'22/23'","'21/22'",
"'20/21'","'19/20'",
"'18/19'","'17/18'",
"'16/17'","'15/16'",
"'14/15'","'13/14'",
"'12/13'","'11/12'",
"'10/11'","'09/10'","'0'",
"'Pre 09/10'"]
season_list.insert(0,"All")

season = st.sidebar.multiselect(
    "Filter by Stay Season:",
    options=season_list,
    default=["'23/24'"])

if "All" in season:
    season = df["Season"].unique().tolist()


shortcut = st.sidebar.multiselect(
    "Season/Month/7 Days Filter",
    options=["MTD","Last 7 Days"])


if shortcut:
    if shortcut[0] == "Last 7 Days":

        today = date.today()

        df = df[df.Created.dt.date > (today - datetime.timedelta(days=7))]

    if shortcut[0] == "MTD":
        
        today = date.today()
        month = today.month
        df = df[df.Created.dt.date > (today - datetime.timedelta(days=35))]
        df = df[df.Created.dt.month==month]

## Finish the side bar ##




df_selection = df.query(
        "Season == @season")


winter_gross = int(df_selection["Gross"].sum())
winter_avg_gross = int(df_selection[df_selection.Gross != 0].Gross.mean())

### Next lets do by booking month

ota_winter_gross = int(df_selection[df_selection.ChannelAS1 == "OTA"]["Gross"].sum())
ota_winter_avg_gross = int(df_selection[(df_selection.Gross != 0)&(df_selection.ChannelAS1=="OTA")].Gross.mean())
ota_per = ota_winter_gross/winter_gross


direct_winter_gross = int(df_selection[df_selection.ChannelAS2 == "Direct"].Gross.sum())
direct_winter_avg_gross = int(df_selection[(df_selection.Gross != 0)&(df_selection.ChannelAS2=="Direct")].Gross.mean())
direct_per = direct_winter_gross/winter_gross

### Split by channel

agent_winter_gross = int(df_selection[df_selection.ChannelAS2 == "Agent"].Gross.sum())
agent_winter_avg_gross = int(df_selection[(df_selection.Gross != 0)&(df_selection.ChannelAS2=="Agent")].Gross.mean())
agent_per = agent_winter_gross/winter_gross


# ota_winter_avg_gross = float(df_selection[(~df_selection.Gross.isnull())&(df_selection.ChannelAS2=="OTA")].Gross.mean())


# df['column_name'].astype(np.float).astype("Int32")







# # TOP METRICS
# total_net = int(df_selection["Net"].sum())
# total_gross = int(df_selection["Gross"].sum())
# total_nights = int(df_selection["Nights"].sum())
# avg_gross = round(df_selection[("Gross")].mean(),0)
# avg_nights = round(df_selection[("Nights")].mean(),0)
top_column1,top_column2,top_column3 = st.columns(3)


path = 'Bookings Clean.csv'
  
# Get the ctime  
# for the specified path 
try: 
    c_time = os.path.getctime(path) 

except OSError: 
    print("Path '%s' does not exists or is inaccessible" %path) 
    sys.exit() 
local_time = time.ctime(c_time)[4:] 
# local_time 
with top_column2:
    st.markdown(f"{local_time}")

    st.markdown(f"#### {season[0][1:-1]} Season ####")
    st.markdown(f"#### Bookings - {df_selection.shape[0]} ####")    
    st.markdown(f"#### Gross Sales ¥{winter_gross:,} ####")
    st.markdown(f"#### Avg/booking ¥{winter_avg_gross:,} ####")







st.divider()

left_column, middle_column, right_column = st.columns(3)


with left_column:

    st.markdown(f"#### Agent - {round(agent_per*100,1)}%")
    st.subheader(f"¥{agent_winter_gross:,}")
    # st.subheader(f"¥{agent_winter_gross:,}")#     st.subheader("Total Gross:")
    st.subheader(f"Avg/booking: ¥ {agent_winter_avg_gross:,}")
    st.markdown("---------")

with middle_column:
    st.subheader(f"Website  -  {round(direct_per*100,1)}%")
    st.subheader(f"¥{direct_winter_gross:,}")#     st.subheader("Total Gross:")
    st.subheader(f"Avg/booking: ¥{direct_winter_avg_gross:,}")
    st.markdown("---------")
    
    
    
    
with right_column:
    st.subheader(f"OTA - {round(ota_per*100,1)}%")
    st.subheader(f"¥{ota_winter_gross:,}")#     st.subheader("Total Gross:")
    st.subheader(f"Avg/booking: ¥ {ota_winter_avg_gross:,}")
    st.markdown("---------")
    
# data = df_selection.groupby(["Booking Month","ChannelAS1"], as_index=False)["Gross"].sum()
# plot = sns.lineplot(data=data, x='Booking Month', y='Gross', hue='ChannelAS1')

# st.plotly_chart(plot)


# fig_gross_channel = px.line(
#     data,
#     x="Booking Month",
#     y = "Gross",
#     hue="ChannelAS1",
#     orientation="h",
#     title="<b>Gross by Channel</b>",
#     template="plotly_white"
#     )
# st.plotly_chart(fig_gross_channel)
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from datetime import date
# df = pd.read_csv("../Downloads/Bookings Clean.csv")
# df["Created"] = pd.to_datetime(df["Created"])

seasons =  ["'22/23'", "'23/24'","'17/18'","'18/19'"]

# df = df[df.Season.isin(seasons)]
# fig = plt.figure(figsize=(9,7))

# sns.lineplot(data=df, x="Booking Month", y="Gross",hue="Season",ci=None,estimator='sum')   
# st.pyplot(fig)

