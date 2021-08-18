"""
Created on Sat Aug 14 18:13:36 2021

@author: frank
"""

import numpy as np
import pandas as pd
import streamlit as st


#Variables
read = pd.read_csv('vehicles.csv')
file = read.sort_values(by = 'price')
url = file['url']
region = file['state']
price = file['price']
year = file['year']
manufacturer = (file['manufacturer'])
model = file['model']
condition = file['condition']
color = file['paint_color']
types = file['type']
image = file["image_url"]
description = file['description']

def sortby(x):
    file = read.sort_values(by = x)
    
sortby('year')

 #Multi-selects
regions = dict()
for r in region:
    if r not in regions:
        regions[r] = 1
    elif r in regions:
        pass
        

colors = dict()
for c in color:
    if c not in colors:
            colors[c] = 1
    elif c in colors:
        pass

manufacturers = dict()
for m in manufacturer:
    if m not in manufacturers:
        manufacturers[m] = 1
    elif m in manufacturers:
        pass

typess = dict()
for t in types:
    if t not in typess:
        typess[t] = 1
    elif t in typess:
        pass
    

#streamlit
st.title("**Welcome**")

st.subheader("Search and then choose from the options below")  
 
#Filters
st.sidebar.write("**Filters**")
yearslider = st.sidebar.slider("Pick oldest year for car",1900,2022)

    
condition_slider = st.sidebar.select_slider("Choose the condition",options=["fair","good","excellent","new"])

    
price_range = st.sidebar.slider("Choose the maximum price",0,100000)
    
   
region_choice = st.sidebar.multiselect("Select state if any", regions.keys())

        
color_choice = st.sidebar.multiselect("Choose color if any", colors.keys())

    
manufacturer_choice = st.sidebar.multiselect("Select manufacturer if any", manufacturers.keys())

    
type_choice = st.sidebar.multiselect("Select a type if any",typess.keys())



def search():
    count = 0
    aprice = 0
    df = pd.DataFrame()

    for t in range(len(type_choice)):               
        for c in range(len(color_choice)):
            for r in range(len(region_choice)):
                for m in range(len(manufacturer_choice)):
                    newfile = file[(file.type == type_choice[t]) & 
                                   (file.state == region_choice[r]) & 
                                   (file.manufacturer == manufacturer_choice[m]) & 
                                   (file.paint_color == color_choice[c]) &
                                   (file.price <= price_range) &
                                   (file.year >= yearslider) &
                                   (file.condition == condition_slider)]
                    
                    if newfile.empty == False:
                        newfiles = newfile[['paint_color', 'region','model','price','manufacturer','type']]
                        df.append(newfile[['paint_color', 'region','model','price','manufacturer','type']])
                        count += len(newfile)
                        df = df.append(newfile) 
                        st.write(f"Showing results for: *{manufacturer_choice[m]}*,*{color_choice[c]}*,*{type_choice[t]}*")
                        for index, row in newfiles.iterrows():
                            #st.write(row.astype('str'))
                            #st.write(f"${newfile['price'][index]:.2f}",f"{newfile['manufacturer'][index]}",f"{newfile['model'][index]}")
                            aprice += newfile['price'][index]
                            col1, col2 = st.columns(2)
                            with col1:                                
                                with st.expander(f"{newfile['manufacturer'][index].upper()} {newfile['model'][index]}"):
                                    
                                    st.write(f"**Price:** ${newfile['price'][index]:,.2f} \t",f"**Year:** {newfile['year'][index]:>20.0f}")
                                    st.write(f"**Color:** {newfile['paint_color'][index]} \t", f"**Type:** {newfile['type'][index]:>20}")
                                    st.write(f"**Location:** {newfile['region'][index]}, {newfile['state'][index].upper()} \t",f"**Condition:** {newfile['condition'][index]}")
                                    st.write(f"[Purchase here]({newfile['url'][index]})")
                            with col2:
                                with st.expander("Description"):
                                    st.write(f"{newfile['description'][index]}")

                            
                    elif newfile.empty == True:
                        pass
    st.write(f"Total results found: {count}")
    averages = df.mean(axis = 'index')
    st.write(f"**Average Price: ** ${averages ['price']:,.2f}")
    
    with st.expander("See advanced details"):        
        st.table(df[['paint_color', 'region','model','price','manufacturer','type']])
if st.sidebar.button("Search"):
        search()
else:
    pass

