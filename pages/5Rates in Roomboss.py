""""""
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import seaborn as sns



st.set_page_config(layout="wide")


st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

df = pd.read_csv("../../Reports/Period_rates.csv")
df["Bedrooms"] = df["Bedrooms"].astype(str)

df['Bedrooms'] = df['Bedrooms'].str.replace(' ', '')
df = df.drop('Unnamed: 0',axis=1)
df = df.reset_index(drop=True)
# df = df.drop(columns=["Unnamed:0"],axis=1)










st.divider()

#------------- ## SIDE BAR ## -------------
bedrooms_list = df["Bedrooms"].unique().tolist()
bedrooms_list.insert(0,"-All")
bedrooms = st.sidebar.multiselect(
    "Filter by Bedroom:",
    options=bedrooms_list,
    default="-All"
    )
if "-All" in bedrooms:
    bedrooms = df["Bedrooms"].unique().tolist()



df_selection = df.query(
   "Bedrooms==@bedrooms")

st.divider()
st.markdown(f"Number of rooms: {df_selection.shape[0]}")




st.dataframe(df_selection,2200,800)


# heapper = sns.heatmap(df_selection,annot=True)

# st.write(heapper,use_container_width=False)



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