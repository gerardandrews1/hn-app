# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 17:31:22 2023

@author: andre
"""

from tkinter import N
import datetime
import time
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException



st.set_page_config(page_title="HN Stuff",
                   page_icon=":bar_chart:",
                   layout="wide"
 )




df = pd.DataFrame()
def niseko_central(
                check_in,check_out,
                adults):
    """Provide basically a competitors API
       for HN and others to use """
    
    check_in = check_in
    check_out =check_out
    adults = adults
#     children = children
    prop_dict = {}

    nights = (pd.to_datetime(check_out) - pd.to_datetime(check_in)).days
    
    
    # TODO Add bedroom option
    columns = ["Room","Total Rate","Bedrooms","Bathrooms",
               "Size - m²","Distance to lifts (m)","Distance to Village (m)"]

    driver = webdriver.Chrome()

    driver.get(f"https://reservations.nisekocentral.com/en/?src=ws\
               &check-in={check_in}&check-out={check_out}&adults={adults}")


    time.sleep(10)
    # Make my soup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    
    # Scrape the info of interest
    rates = soup.find_all("div",class_="nR4hmu2D-OTMdFG-NxDMbA==")
    properties = soup.find_all("div",class_="Zb3b+V1AKSfEtcHNrUqDJg==")
    rooms = soup.find_all("div",class_="-KXBRBUV04+nmC64J5Ls+A==")
    beds_baths = soup.find_all("div",class_="idEmDHYiqL6JNPXm8K-YNg==")
    sizes = soup.find_all("div",class_="N+VWc8LnI7cY6FLvSUC89Q==")


    # Loop through each property and assign values to dict
    for i in range(0,len(rates),1):

        rate =  rates[i].text
        propertay = properties[i].text
        room = rooms[i].text
        bedrooms = beds_baths[i].text.split(',')[0]
        bathrooms = beds_baths[i].text.split(',')[1].split("Beds")[0]
        size = sizes[i].text.split("sqm")[0].split("size:")[1]
        
        lift_dist = sizes[i].text.split('Village')[0][-4:]
        lift_dist = lift_dist.split("m")[0]
        village_dist = sizes[i].text.split("Centre within")[-1].split("m")[0]
        

        prop_dict[propertay+ "---" +room] = [room,rate,bedrooms,bathrooms,size,lift_dist,village_dist]

        
    df = pd.DataFrame.from_dict(prop_dict,orient ='index',columns=columns) 
    df["Company"] = "NisekoCentral"
    df["Bedrooms"] = df["Bedrooms"].astype(str).str.replace("Bedroom","")
    df["Total Rate"] = df["Total Rate"].astype(str).str.replace("¥","")
    df["Total Rate"] = df["Total Rate"].astype(str).str.replace(",","")

    df["Nights"] = nights
    df["Nightly Rate"] = df["Total Rate"].astype(int)/nights
    

    df = df.reset_index()
    df = df.rename(columns={'index': 'Property'})
    df["Property"] = df["Property"].astype(str).str.split("---").str[0]
    df = df[["Property","Room","Nightly Rate","Total Rate","Bedrooms","Company"]]

    
    return df



def vn_niseko_fuckya(check_in,check_out,
                    adults):
    
    """Provide a competitors analysis API
       for HN and others to use tokatoka """
    
    check_in = check_in
    check_out = check_out
    adults = adults

    nights = (pd.to_datetime(check_out) - pd.to_datetime(check_in)).days
    
    
    # TODO Add bedroom option*
    columns = ["Room","Nightly Rate","Bedrooms","Bathrooms"]
    
    
    driver = webdriver.Chrome()
    
    driver.get(f"https://vacationniseko.com/en/accommodation?currency=jpy")

#     driver.get(f"https://vacationniseko.com/en/accommodation")
    time.sleep(3)
    
    
  
    
    # Find element
    # Remove the attributes (takes the value)
    # Elements changed state we need to get again
    # Finally change date to our date
    
    
    stdt_box = driver.find_element(By.CLASS_NAME,value="checkin-at-field")
    driver.execute_script("arguments[0].removeAttribute('type')", stdt_box)
    new_stdt_box = driver.find_element(By.CLASS_NAME,value="checkin-at-field")
    driver.execute_script(f"arguments[0].setAttribute('value','{check_in}')", new_stdt_box)
    
    
    eddt_box = driver.find_element(By.CLASS_NAME,value="checkout-at-field")
    driver.execute_script("arguments[0].removeAttribute('type')", eddt_box)
    new_eddt_box = driver.find_element(By.CLASS_NAME,value="checkout-at-field")
    driver.execute_script(f"arguments[0].setAttribute('value','{check_out}')", new_eddt_box)
    
    driver.find_element(By.CLASS_NAME,value="checkout-at-field").send_keys(Keys.ENTER)

    
    time.sleep(10)
    
   
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    
 
    
    cards = soup.find_all("div",class_= "card card-property rb-filtered")
    print(len(cards))
    prices = soup.find_all("div",class_= "property-price")

    
    prop_list = []
    prop_dict = {}
    
    for c in cards:
        property_title = c.find('h3').text
        
        rooms = c.find_all("div",class_="property-pricing-table-item available")
        
        
        for room in rooms:

            room_type = room.find("p",class_="room-title")
            price = room.find("span",class_="room-price d-md-none")
            price = price.text.split("/night")[0].strip()
            
            ammen = room.find("ul", class_="ammendities").text
            ammen = ammen.split("  ")
            
            bedrooms = ammen[1].strip()
            bathrooms = ammen[3]
            
            
            prop_dict[property_title] = [room_type.text,price,bedrooms,bathrooms]
#            
    
    df = pd.DataFrame.from_dict(prop_dict,orient ='index',columns=columns) 

    df["Company"] = "VacationNiseko"
    
    df["Nights"] = nights
    
    df["Rate P"] = df["Nightly Rate"].astype(str).str.replace("¥","")
    df["Rate P"] = df["Rate P"].astype(str).str.replace(",","")
    df["Total Rate"] = df["Nights"]*df["Rate P"].astype(int)
    
    df["Nightly Rate"] = df["Nightly Rate"].str.replace("¥","")
    df["Nightly Rate"] = df["Nightly Rate"].str.replace(",","")

    df = df.drop("Rate P", axis=1)
    df = df.reset_index()
    df = df.rename(columns={'index': 'Property'})
    df = df[["Property","Room","Nightly Rate","Total Rate","Bedrooms","Bathrooms","Company"]]
    
    
    return df








def airbnb_hirafu(check_in,check_out,adults):
    """
    Scrape Airbnb for Hirafu search
    get results to df
    
    """
    check_in = check_in
    check_out = check_out
    adults = adults
    prop_dict = {}
    columns = ["Room","Nightly Rate","Total Rate"]

    nights = (pd.to_datetime(check_out) - pd.to_datetime(check_in)).days 
    
    # airbnb_search = f"""https://www.airbnb.com/s/hirafu/homes?tab_id=home_tab&\
    #                      refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D\
    #                      =one_week&price_filter_input_type=0&price_filter_num_nights={nights}&\
    #                      channel=EXPLORE&date_picker_type=calendar&adults={adults}&source=\
    #                      structured_search_input_header&search_type=filter_change&\
    #                      checkin={check_in}&checkout={check_out}&monthly_start_date=2023-10-01&\
    #                      monthly_length=3&query=Hirafu%2C%20Kutchan%2C%20Hokkaido%2C%20Japan"""
    print(check_in)
    airbnb_search2 = f"""https://www.airbnb.com/s/Hirafu--Kutchan--Abuta-District--Japan/homes?adults={adults}\
                  &place_id=ChIJM7U2tkSwCl8RRlVXnoXXMmk&refinement_paths%5B%5D=%2Fhomes&checkin={check_in}&checkout={check_out}"""
    
    # https://www.airbnb.com/s/Hirafu--Kutchan--Abuta-District--Japan/homes?adults=1&place_id=ChIJM7U2tkSwCl8RRlVXnoXXMmk&refinement_paths%5B%5D=%2Fhomes&checkin=2024-01-05&checkout=2024-01-10


    driver = webdriver.Chrome()
    
    
    driver.get(airbnb_search2)
    time.sleep(10)
    
    
    listing_dict = {}
    # Write a big for loop to check the number of pages and then move through them slow
    
    for results_page in range(0,20,1):
        
        html = driver.page_source

    
        soup = BeautifulSoup(html, 'html.parser')



        cards = soup.find_all("div",class_="dir dir-ltr")
        for c in cards:

            try:
                name = c.find("div",class_="fb4nyux s1cjsi4j dir dir-ltr")
                descrip = c.find("div",class_="t1jojoys dir dir-ltr")
                price = c.find("div",class_="_1jo4hgw")
                total_price = c.find("div",class_="_tt122m")
                
                if name:
                    listing_dict[name.text] = [descrip.text,price.text,total_price.text]

                    

            except Exception as e:
                print("HEYA")
                print(e)

        try:
            pages = driver.find_element(By.XPATH,value="//a[@aria-label='Next']").click()
            time.sleep(6)

        except Exception as e:
            break
    
    
    df = pd.DataFrame.from_dict(listing_dict,orient ='index',columns=columns) 
    df = df.reset_index()

    df["Nightly Rate"] = df["Nightly Rate"].astype(str).str.replace("night","")
    df["Total Rate"] = df["Total Rate"].astype(str).str.replace("total","")
    df["Nightly Rate"] = df["Nightly Rate"].str[-9:]
    df["Nightly Rate"] = df["Nightly Rate"].str.replace("¥","")
    df["Nightly Rate"] = df["Nightly Rate"].str.replace(",","")

    df["Total Rate"] = df["Total Rate"].str.replace("¥","")
    df["Total Rate"] = df["Total Rate"].str.replace(",","")
    df = df.rename(columns={'index': 'Property'})
    
    df["Company"] = "Airbnb"

    
    return df




def dummy_function(check_in,check_out,guests):
    
    """IM A DUMMY"""
    ab_df = airbnb_hirafu(check_in,check_out,guests) 
    df = niseko_central(check_in,check_out,guests)
    df2 = vn_niseko_fuckya(check_in,check_out,guests)


    join_df = pd.concat([df,df2,ab_df])
    join_df["Nightly Rate"]= join_df["Nightly Rate"].astype(int)

    join_df.to_csv("Central, VN and Airbnb.csv",encoding='utf-8-sig')
    return join_df


checkin_input = st.text_input("Check in")
checkout_input = st.text_input("Check out")
adults = st.text_input("Adults")

if st.button("Get prices"):
    output_df = dummy_function(checkin_input,checkout_input,adults)
    time.sleep(5)
    # st.dataframe(output_df)
    st.markdown(f"Available Properties: {output_df.shape[0]}")


# run = st.text_input("Enter to run")

# if run:
#     df = niseko_central(checkin_input,checkout_input,adults,children,False)
#     # df = niseko_central("2024-03-11","2024-03-16","2","0",False)
#     time.sleep(5)
#     st.markdown("Available Properties: " + str(df.shape[0]))



# -----------------Show df--------------#

try:
    st.dataframe(output_df,1000,800)


except:
    print("df_error")


# -------------Download button-------------#


# def convert_df(df):
#     return output_df.to_csv(index=False).encode('utf-8')


    
# csv = convert_df(output_df)

# st.download_button(
#     "Press to Download",
#     csv,
#     "Your Download.csv",
#     "text/csv",
#     key='download-csv'
#     )
    