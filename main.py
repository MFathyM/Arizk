# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 19:35:24 2022

@author: DELL
"""

#package installation
import pandas as pd
import streamlit as st
import plotly.express as px
import pyrebase

from datetime import datetime

#Title and Header
st.set_page_config(page_title='Arizk Force')
st.header('Arizk Force')

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

#Importing Data
kpiData = fbChildToDf("KPIs")
visitData = fbChildToDf("Visits")
activityData = fbChildToDf("Activities")
offerData = fbChildToDf("Offers")
userData = fbChildToDf("Users")

#Convert dates into datetime
kpiDates = kpiData['date'].tolist()
kpiDatesEdited = []
for kpiDate in kpiDates:
    kpiDatesEdited.append(kpiDate[0:8])
kpiData['date']=kpiDatesEdited
kpiData['date'] = kpiData['date'].apply(lambda x: datetime.strptime(x, '%d/%m/%y'))
visitData['date'] = visitData['date'].apply(lambda x: datetime.strptime(x, '%d/%m/%y %H:%M:%S'))
activityData['date'] = activityData['date'].apply(lambda x: datetime.strptime(x, '%d/%m/%y'))
offerData['offerDate'] = offerData['offerDate'].apply(lambda x: datetime.strptime(x, '%d/%m/%y'))
offerDF = offerData['offerDate']
offerDF.rename("date")

#Filter Date Inputs
dates = [kpiData['date'], visitData['date'], activityData['date'], offerDF]
dates = pd.concat(dates)
startDate=st.date_input("Start Date", value=min(dates))
startDate=startDate.strftime('%d/%m/%y')
endDate=st.date_input("End Date")
endDate=endDate.strftime('%d/%m/%y')

#Filter Drop Down users
userNames = userData['userName'].tolist()
userNames.append('All')
userNames.remove('Guest')
selectedUser = st.selectbox('Select User',userNames, index = userNames.index('All'))

#Filter dataframes by date
def filterDfByDate(df1, start_date, end_date, date_string):
    df2 = df1[(df1[date_string]>=datetime.strptime(start_date, '%d/%m/%y'))]
    if not df2.empty:
        df2 = df2[(df2[date_string]<=datetime.strptime(end_date, '%d/%m/%y'))]
    return df2

#Filter dataframes by user name
def filterDfByName(dfa, selected_user, user_string):
    dfb=dfa
    if not selected_user=='All' and not dfa.empty:
        dfb = dfa[(dfa[user_string]==selected_user)]
    return dfb

#KPI Visualization
st.subheader('KPI Visualization')
kpiDataFiltered = filterDfByDate(kpiData, startDate, endDate, 'date')
kpiDataFiltered = filterDfByName(kpiDataFiltered, selectedUser, 'userName')
if not kpiDataFiltered.empty:
    kpiSums = kpiDataFiltered.groupby(['userName'])['kpi'].sum()
    kpiBarChart = px.bar(kpiSums,
                    x=kpiSums.index,
                    y='kpi',
                    color_discrete_sequence=['#F63366']*len(kpiSums),
                    template='plotly_white')
    st.plotly_chart(kpiBarChart)
    st.dataframe(kpiDataFiltered)
else:
    st.write('No data available in this time range')

#Visit Visualization
st.subheader('Visit Visualization')
visitDataFiltered = filterDfByDate(visitData, startDate, endDate, 'date')
visitDataFiltered = filterDfByName(visitDataFiltered, selectedUser, 'userName')
if not visitDataFiltered.empty:
    visitCounts = visitDataFiltered['userName'].value_counts()
    visitBarChart = px.bar(visitCounts,
                    x=visitCounts.index,
                    y='userName',
                    color_discrete_sequence=['#F63366']*len(visitCounts),
                    template='plotly_white')
    st.plotly_chart(visitBarChart)
    st.dataframe(visitDataFiltered)
else:
    st.write('No data available in this time range')

#Activity Visualization
st.subheader('Activity Visualization')
activityDataFiltered = filterDfByDate(activityData, startDate, endDate, 'date')
activityDataFiltered = filterDfByName(activityDataFiltered, selectedUser, 'userName')
if not activityDataFiltered.empty:
    activityCounts = activityDataFiltered['userName'].value_counts()
    activityBarChart = px.bar(activityCounts,
                    x=activityCounts.index,
                    y='userName',
                    color_discrete_sequence=['#F63366']*len(activityCounts),
                    template='plotly_white')
    st.plotly_chart(activityBarChart)
    st.dataframe(activityDataFiltered)
else:
    st.write('No data available in this time range')

#Offer Visualization
st.subheader('Offer Visualization')
offerData = offerData[offerData['offerNumber']!="0"]
offerDataFiltered = filterDfByDate(offerData, startDate, endDate, 'offerDate')
offerDataFiltered = filterDfByName(offerDataFiltered, selectedUser, 'offerUserName')
if not offerDataFiltered.empty:
    offerCounts = offerDataFiltered['offerUserName'].value_counts()
    offerBarChart = px.bar(offerCounts,
                    x=offerCounts.index,
                    y='offerUserName',
                    color_discrete_sequence=['#F63366']*len(offerCounts),
                    template='plotly_white')
    st.plotly_chart(offerBarChart)
    st.dataframe(offerDataFiltered)
else:
    st.write('No data available in this time range')
    
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

