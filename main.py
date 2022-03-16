# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 19:35:24 2022

@author: DELL
"""

#package installation
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import pyrebase
import requests

#Title and Header
st.set_page_config(page_title='Arizk Force')
st.header('Arizk Force')
url = 'https://github.com/MFathyM/Arizk/blob/574005c44de95889e3e6173ccafb5bf475471927/logo.PNG'
Image.open(requests.get(url, stream=True).raw)

#API configuration of firebase
firebaseConfig={'apiKey': "AIzaSyAc1i1S9nU3Zg6X_5j0uH4X2JmJXAPLW5w",
  'authDomain': "arizk-d81e8.firebaseapp.com",
  'databaseURL': "https://arizk-d81e8-default-rtdb.firebaseio.com",
  'projectId': "arizk-d81e8",
  'storageBucket': "arizk-d81e8.appspot.com",
  'messagingSenderId': "768017715011",
  'appId': "1:768017715011:web:25ea2a622817634ad869f6",
  'measurementId': "G-8LS842XX6P"}
firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()

#Convert a child name to pandas dataframe
def fbChildToDf(childName):
    items = db.child(childName).get()
    itemList=[]
    for item in items.each():
        itemList.append(item.val())
    return pd.DataFrame(itemList)

#KPI Visualization
st.subheader('KPI Visualization')
kpiData = fbChildToDf("KPIs")
kpiSums = kpiData.groupby(['userName'])['kpi'].sum()
kpiBarChart = px.bar(kpiSums,
                    x=kpiSums.index,
                    y='kpi',
                    color_discrete_sequence=['#F63366']*len(kpiSums),
                    template='plotly_white')
st.plotly_chart(kpiBarChart)
st.dataframe(kpiData)

#Visit Visualization
st.subheader('Visit Visualization')
visitData = fbChildToDf("Visits")
visitCounts = visitData['userName'].value_counts()
visitBarChart = px.bar(visitCounts,
                    x=visitCounts.index,
                    y='userName',
                    color_discrete_sequence=['#F63366']*len(kpiSums),
                    template='plotly_white')
st.plotly_chart(visitBarChart)
st.dataframe(visitData)

#Activity Visualization
st.subheader('Activity Visualization')
activityData = fbChildToDf("Activities")
activityCounts = activityData['userName'].value_counts()
activityBarChart = px.bar(activityCounts,
                    x=activityCounts.index,
                    y='userName',
                    color_discrete_sequence=['#F63366']*len(kpiSums),
                    template='plotly_white')
st.plotly_chart(activityBarChart)
st.dataframe(activityData)

#Offer Visualization
st.subheader('Offer Visualization')
offerData = fbChildToDf("Offers")
offerCounts = offerData['offerUserName'].value_counts()
offerBarChart = px.bar(offerCounts,
                    x=offerCounts.index,
                    y='offerUserName',
                    color_discrete_sequence=['#F63366']*len(kpiSums),
                    template='plotly_white')
st.plotly_chart(offerBarChart)
st.dataframe(offerData)

#Authentication
#auth=firebase.auth()
#login
#email=input("Enter your email")
#password=input("Enter your password")
#try:
#    auth.sign_in_with_email_and_password(email, password)
#   print("Successfully signed in")
#except:
#    print("Invalid username or password")

#storage=firebase.storage()

