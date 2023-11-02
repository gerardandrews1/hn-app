import io
import json
import pandas as pd
import requests
import streamlit as st
from pandas.io.json import json_normalize
from ratelimit import limits, sleep_and_retry

st.set_page_config(layout="wide")

def highlight(s):
    """ Used to colour payment df if not paid """
    if s["Payment Date"] == None:
        return ['background-color: #ffb668'] * len(s)
    else:
        return ['background-color: white'] * len(s)



col1, col2 = st.columns(2)
json_string = None


# Set API call limit 
three_mins = 180

@limits(calls=15, period=three_mins)
def call_api(ebook_id):
    
    """
    Send request to API
    Wrapper 15 calls per 3 min limit 
    imposed. 
    Using HN API credentials
    """

    url = "https://api.roomboss.com/extws/hotel/v1/listBooking?bookingEid="+ebook_id
    
    auth = ('holidayniseko',"Deo6FYvVgtcmQMTU")
    
    response = requests.get(url,auth=auth)

    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response


with col1:
    user_input = st.text_input("Input booking ID")

user_input = user_input.strip()
   
if len(user_input) == 7 :
    
    try:
        response = call_api(user_input)

        json_string = json.loads(response.text)
        
    except Exception:
        print(Exception)
    
else:
    st.markdown("Not a valid ID")

# Create a df to append to later
booking_df = pd.DataFrame(columns=["Check In","Check Out","Nights","Guests",
                                    "Property","Room","Rate"])


if json_string:   

    gs_df = pd.DataFrame(columns=["Service Provider","Start Date","Total Cost"])
    booking_cost = 0
    for booking in json_string.get("order",{}).get("bookings",{}):

        if booking.get('bookingType',{})=="ACCOMMODATION":


            bid = json_string['order']['bookings'][0]['bookingId']
            # easy_link = "https://app.roomboss.com/ui/booking/edit.jsf?bid=" + bid 

            # example_dict.get('key1', {}).get('key2')

            propertay = json_string.get("order",{}).get("bookings",
                                {})[0].get("hotel",{}).get("hotelName",
                                {})

            room = json_string.get("order",{}).get("bookings",
                                {})[0].get("items",{})[0].get("roomNumber",{})


            guests = json_string.get("order",{}).get("bookings",
                                {})[0].get("items",{})[0].get("numberGuests",{})

            rate = json_string.get("order",{}).get("bookings",
                                {})[0].get("items",{})[0].get("priceRetail")
            

            rate = int(rate)
            booking_cost += rate
            rate = f'¥{rate:,}'

            check_in = json_string.get("order",{}).get("bookings",
                                {})[0].get("items",{})[0].get("checkIn",{})

            check_out = json_string.get("order",{}).get("bookings",
                                {})[0].get("items",{})[0].get("checkOut",{})

            email = json_string.get('order',{}).get('leadGuest',{}).get('email',{})

            given_name = json_string.get('order',{}).get('leadGuest',{}).get('givenName')
            family_name = json_string.get('order',{}).get('leadGuest',{}).get('familyName')
            name = f"{given_name} {family_name}"
            
            with col1:
                st.markdown(name)
            dt_check_in = pd.to_datetime(check_in)

            dt_check_out = pd.to_datetime(check_out)

            check_in = check_in.replace("-","/")
            check_out = check_out.replace("-","/")

            nights = (dt_check_out - dt_check_in).days

            # Create a list to append to df
            booking_line = [check_in,check_out,nights,guests,propertay,room,rate]
            booking_df.loc[len(booking_df)] = booking_line


            with col2:
                st.markdown(booking_df.style.hide(axis="index")
                        .set_table_styles([{'selector': 'th', 'props': [('font-size', '10pt'),('text-align','center')]}])
                        .set_properties(**{'font-size': '8pt','text-align':'center'}).to_html(),unsafe_allow_html=True)
                st.markdown(" ")



        ## Guest Service Part ##
        elif booking.get('bookingType',{})=="SERVICE":
            
            line_item = []
            line_item.append(booking.get("serviceProvider",{}).get("serviceProviderName",{}))
            line_item.append(booking.get("items",{})[0].get("startDate",{}))

            total_cost = 0
            for item in booking.get("items"):
                total_cost += int(item.get("priceRetail"))

            line_item.append(f"¥{total_cost:,}")


            # line_item.append(st.link_button("Launch Extra",f"https://app.roomboss.com/ui/booking/edit.jsf?bid={booking_id}"))
            gs_df.loc[len(gs_df)] = line_item
            booking_cost += total_cost
    with col1:
        ## Create the strings for emails ##

        if email:
            st.markdown(email)
        with col2:
            email_string = f"""{propertay} Booking #{user_input} ~ {check_in} - {check_out} ~ ({guests} guests, {nights} nights)"""
            st.markdown(email_string)

        
        roomboss_url =  f"https://app.roomboss.com/ui/booking/edit.jsf?bid={bid}"
        st.markdown("[Go to booking in Roomboss](%s)" % roomboss_url)



        ## Create the links ##
# Old Guest services link https://holidayniseko.evoke.jp/public/booking/order02.jsf?mv=1&vs=Guestservices&bookingEid={user_input}"
        payment_df = pd.DataFrame(columns=["Invoice No","Due Date","Invoice Amount",
                                           "Payment Amount","Payment Date","Payment ID"])
        if email:

            gsg_link = f"https://holidayniseko2.evoke.jp/public/booking/order02.jsf?mv=1&vs=Guestservices&bookingEid={user_input}"
            payment_link = f"https://holidayniseko.evoke.jp/public/yourbooking.jsf?id={user_input}&em={email}"
            st.markdown("[Self serve guest services link](%s)" % gsg_link)
            st.markdown("[Payment link](%s)" % payment_link)

        invoiced = 0
        paid = 0
        invoices = json_string.get("order",{}).get("invoicePayments")
        for invoice in invoices:
            
            amount = invoice.get("invoiceAmount")
            amount = int(amount)
            invoiced += amount
            # booking_cost += invoiced
            invoice_number = invoice.get("invoiceNumber")

            amount = f'¥{amount:,}'
            
            due_date = invoice.get("invoiceDueDate")

            payment_amount = invoice.get("paymentAmount")
       

            payment_amount = int(payment_amount)
            paid += payment_amount
            # booking_cost -= payment_amount

            payment_amount = f'¥{payment_amount:,}'
            payment_date = invoice.get("paymentDate")
            payment_id = invoice.get("paymentId")

            
            payment_line = [invoice_number,due_date,amount,payment_amount,payment_date,payment_id]
            
            payment_df.loc[len(payment_df)] = payment_line
            payment_df.reset_index(drop=True,inplace=True)


    if payment_df.shape[0] > 0:
        
                    
        with col2:
            # st.table(payment_df)
            st.markdown(payment_df.style.hide(axis="index")
                    .apply(highlight,axis=1)
                    .set_table_styles([{'selector': 'th', 'props': [('font-size', '10pt'),('text-align','center')]}])
                    .set_properties(**{'font-size': '10pt','text-align':'center'}).to_html(),unsafe_allow_html=True)
            st.markdown(" ")
            st.markdown(f"¥{invoiced:,} invoiced and ¥{paid:,} paid")
            st.markdown(f"**¥{invoiced - paid:,} owing**")
            st.divider()
            st.markdown(gs_df.style.hide(axis="index")
                                    .set_table_styles([{'selector': 'th', 'props': [('font-size', '10pt'),('text-align','center')]}])
                                    .set_properties(**{'font-size': '10pt','text-align':'center'}).to_html(),unsafe_allow_html=True)
            # st.markdown(gsg_total)
            

    else:
        with col2:
            st.markdown("**No Invoices**")
            st.markdown(gs_df.style.hide(axis="index")
                                    .apply(highlight,axis=1)
                                    .set_table_styles([{'selector': 'th', 'props': [('font-size', '10pt'),('text-align','center')]}])
                                    .set_properties(**{'font-size': '10pt','text-align':'center'}).to_html(),unsafe_allow_html=True)
#         pprint.pprint(invoices)

    with col1:
        st.markdown(f"**Cost of booking ¥{booking_cost:,}**")
        st.markdown(f"**Invoiced on booking ¥{invoiced:,}**")
# payment_df.style.apply(highlight,axis=1)


st.divider()

prop_url = "https://docs.google.com/document/d/1pgRIOGFoOwALqThPm1VOo5a8lwpzkZiCxTW-sh-i2pw/edit?usp=sharing"
# st.markdown(prop_link,unsafe_allow_html=True)
prop_link = st.link_button("Property Spiels", prop_url)




gsg_url= "https://holidayniseko.com/sites/default/files/services/2023-08/Holiday%20Niseko%20Guest%20Service%20Guide%202023_2024.pdf"
gsg_link = st.link_button("Guest Services Guide", gsg_url)

hn_tasks_url = "https://docs.google.com/spreadsheets/d/1zIkN35Z-3xUrD1rm4ru2ssC6h-cpTTgs0LNptnjmZms/edit?usp=sharing)"
hn_tasks_link = st.link_button("HN Tasks Google Sheets",hn_tasks_url)

email_spiels_url = "https://docs.google.com/document/d/119EWDec3PDV8SIWkpjVcjXHpkJB_bsPBxMk0yfiHfmI/edit?usp=sharing"
email_spiels_link = st.link_button("Email Spiels",email_spiels_url)

# st.markdown("HN Tasks Google Sheet --> https://docs.google.com/spreadsheets/d/1zIkN35Z-3xUrD1rm4ru2ssC6h-cpTTgs0LNptnjmZms/edit?usp=sharing")

