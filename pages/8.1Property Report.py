""""""
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import seaborn as sns



st.set_page_config(layout="wide")


st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

df = pd.read_csv("../../Reports/hn_books.csv")


st.divider()

## --------------- SIDE BAR -----------#
st.sidebar.header("Please filter here:")



property_list = df["Vendor"].unique().tolist()
property_list.insert(0,"-All")




vendor = st.sidebar.multiselect(
    "Filter by Property:",
    options=sorted(property_list, key=str.lower),
    default="-All"     
    )


if "-All" in vendor:
    vendor = df["Vendor"].unique().tolist()


st.markdown(vendor)

if len(vendor) < 30:
    room_df = df[df["Vendor"]==str(vendor[0])]
    room_list = room_df.Product.unique().tolist()

    product = st.sidebar.multiselect(
        "Filter by room:",
        options = room_list
         )
else:
    product = 0
   #  st.markdown(products)

# product = st.sidebar.multiselect(

#     "Filter by Room:",
#     options=room_list

# )


df_selection = df.query("Vendor == @vendor & Product == @product")


st.dataframe(df_selection,2200,800)

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(df)

st.download_button(
   "Press to Download",
   csv,
   "Your Download.csv",
   "text/csv",
   key='download-csv'
)