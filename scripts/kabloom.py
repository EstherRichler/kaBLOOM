#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 18:30:01 2020

@author: esther
"""


import os
import streamlit as st
import numpy as np
import pandas as pd
import datetime
import math

#%%

#get data and put into dataframe

@st.cache
def get_areas():
    
    #load areas
    areas_2017 = np.load(os.environ['PWD'] + 'poppy-finder/data/areas_2017.npz')
    areas_2018 = np.load(os.environ['PWD'] + 'poppy-finder/data/areas_2018.npz')
    areas_2019 = np.load(os.environ['PWD'] + 'poppy-finder/data/areas_2019.npz')
    areas_2020 = np.load(os.environ['PWD'] + 'poppy-finder/data/areas_2020.npz')
    
    #convert from .npz to dictionaries
    areas_2017_dict = {item: areas_2017[item] for item in areas_2017.files}
    areas_2018_dict = {item: areas_2018[item] for item in areas_2018.files}
    areas_2019_dict = {item: areas_2019[item] for item in areas_2019.files}
    areas_2020_dict = {item: areas_2020[item] for item in areas_2020.files}
    
    #merge all years into a single dictionary
    areas_dict = {**areas_2017_dict, **areas_2018_dict, **areas_2019_dict, **areas_2020_dict}
    
    #get list of locations
    location_list = [name.split('_')[1] for name in list(areas_dict)]
    
    #get list of dates (in datetime format)
    date_list = [datetime.datetime.strptime(name.split('_')[0], '%Y-%m-%d') for name in list(areas_dict)]
    
    #get # pixels in the background area
    background_list = [areas_dict[key][0] for key in areas_dict]
    
    #get # of patches
    n_patches_list = [len(areas_dict[key]) -1 for key in areas_dict]
    
    #this is where my list comprehension skills break down and I resort to looping
    patches_list = []
    max_patch_list = []
    for key in areas_dict:
        
        #remove background patch
        tmp = areas_dict[key][1:]
        
        #get total # of pixels from all patch areas
        patches_list.append(sum(tmp))
        
        #get number of pixels in biggest patch (that is not background)
        if sum(tmp)==0:
            max_patch_list.append(0)
        else:
            max_patch_list.append(max(tmp))
            
    #put data into dataframe
    df = pd.DataFrame({'location':location_list, 'background':background_list, 'patches':patches_list, \
                   'n_patches':n_patches_list, 'max_patch':max_patch_list}, index=date_list)
    
    df_antelope = df[df.location=='antelope']
    df_elsinore = df[df.location=='elsinore']
    df_grassmtn = df[df.location=='grassmtn']
    
    return df_antelope, df_elsinore, df_grassmtn

df_antelope, df_elsinore, df_grassmtn = get_areas()


#observed_antelope = pd.read_csv('/home/esther/poppy-finder/data/observations-antelope.csv')
#observed_elsinore = pd.read_csv('/home/esther/poppy-finder/data/observations-elsinore.csv') 

observed_antelope = pd.read_csv(os.environ['PWD'] + 'poppy-finder/data/observations-antelope.csv')
observed_elsinore = pd.read_csv(os.environ['PWD'] + 'poppy-finder/data/observations-elsinore.csv') 
#%%

st.markdown('---')
st.title("kaBLOOM!")
st.markdown('<style>h1{color: orange;}</style>', unsafe_allow_html=True)
st.write('The poppy finding app')
st.markdown('---')
    
#%%

#user selects location
option_loc = st.selectbox(
    'Please select a location',
     ['Lake Elsinore, Riverside County', 'Grass Mountain, Los Angeles County', 'Antelope Valley, Los Angeles County'])

#user selects date
option_date = st.date_input('Please select a date (for demo purposes)', value=datetime.date.today())
year = option_date.year


#%%

#get data and info for selected location and date

if option_loc == 'Lake Elsinore, Riverside County':
    
    df_tmp = df_elsinore
    location = 'Lake Elsinore'
    visit2 = f'[UC Riverside Botanic Gardens](https://gardens.ucr.edu/)'
    visit1 = f'[San Diego Botanic Garden](https://www.sdbgarden.org/)'
    hikes = f'[here](https://www.alltrails.com/us/california/lake-elsinore)'
    directions = f'[here](https://www.google.com/maps/place/Walker+Canyon/@33.7305734,-117.4092181,14z/data=!3m1!4b1!4m5!3m4!1s0x80dc97c4ad774b6b:0xda907af43c25f7ab!8m2!3d33.7305751!4d-117.3917085)'
    
elif option_loc == 'Grass Mountain, Los Angeles County':
    
    df_tmp = df_grassmtn
    location = 'Grass Mountain'
    visit1 = f'[LA Arboretum](https://www.arboretum.org/)'
    visit2 = f'[Descanso Gardens](https://www.descansogardens.org/)'
    hikes = f'[here](https://www.alltrails.com/trail/us/california/grass-mountain)'
    directions = f'[here](https://www.google.com/maps/place/Grass+Mountain/@34.6360441,-118.4776599,12.1z/data=!4m5!3m4!1s0x80c26f5e580c9a29:0x7c8c3f57fd11159d!8m2!3d34.6410977!4d-118.4134145)'
    
elif option_loc == 'Antelope Valley, Los Angeles County':
    
    df_tmp = df_antelope
    location = 'Antelope Valley'
    visit1 = f'[LA Arboretum](https://www.arboretum.org/)'
    visit2 = f'[Descanso Gardens](https://www.descansogardens.org/)'
    hikes = f'[here](https://www.alltrails.com/us/california/lancaster)'
    directions = f'[here](https://www.google.com/maps/place/Antelope+Valley+California+Poppy+Reserve+State+Natural+Reserve/@34.7117001,-118.4264798,13.08z/data=!4m5!3m4!1s0x80c26c00eb7ecc9b:0x582ed8c0bf849de9!8m2!3d34.7249116!4d-118.3969062)'

alltrails = f'[AllTrails.com](https://www.alltrails.com/)'
sheep = f'[here is](https://www.youtube.com/watch?v=UrKkchVOOAs)'

#remove data from after selected date
df_tmp = df_tmp.truncate(after=option_date)

#get current bloom level for location
bloom_level = df_tmp.iloc[-1]['patches']
n_patches = df_tmp.iloc[-1]['n_patches']
max_patch = df_tmp.iloc[-1]['max_patch']


#%%

#user presses button!
b = st.button(label='Find poppies!')

#text responses different scenarios
if b:
    
    
    #January and February
    if option_date.month in [1,2]:
        
        result = f'''Poppy season should be starting in the next few weeks! We'll start looking for blooms at
                  the beginning of March, so be sure to check back then.
                 '''
        st.markdown(result)
        
        naturalist = f'''[iNaturalist.org](https://www.inaturalist.org/observations?%20quality_grade=any&identifications=any&swlat=34.65275197179807&swlng=-118.54212363125656&nelat=34.80793834080253&nelng=-118.20839253818516&taxon_id=48225&d1=2019-04-01&d2=2019-04-30)'''
        
        suggestion = f'''In the meantime, check out {naturalist}
                  to keep an eye on recent poppy sightings in the {location} area.
                 '''
        st.markdown(suggestion)
    
        
    #March, no bloom
    elif option_date.month==3 and bloom_level == 0:
        
        result = '''Our algorithm has not detected a bloom yet. We get new satellite info every few days, so keep checking back for updates!'''
        st.markdown(result)
        
        naturalist = f'''[iNaturalist.org](https://www.inaturalist.org/observations?%20quality_grade=any&identifications=any&swlat=34.65275197179807&swlng=-118.54212363125656&nelat=34.80793834080253&nelng=-118.20839253818516&taxon_id=48225&d1=2019-04-01&d2=2019-04-30)'''
        suggestion = f'''In the meantime, check out {naturalist} 
        to keep an eye on recent poppy sightings in the {location} area.
        '''
        st.markdown(suggestion)
    
    #April, no bloom, no previous bloom    
    elif option_date.month==4 and bloom_level==0 and df_tmp.iloc[-2]['patches']==0:
        
        result = f'''Our algorithm has still not picked up on any blooms in the {location} area, and it looks like this years poppy season is turning out to be a bust. 
        Keep checking back over the next few weeks in case of a late bloom. In the meantime, {sheep} something to help with the disappointment.'''
        st.markdown(result)
        
    #April, no bloom, yes previous bloom    
    elif option_date.month==4 and bloom_level==0 and df_tmp.iloc[-2]['patches']>0:
        
        
        result = f''' Poppy season is now over for {year}. We are sad about this too, 
                 but how about getting your flower fix at the {visit1} or {visit2}? 
                 '''
        st.markdown(result)
    
    #March and April - bloom
    elif option_date.month in [3,4] and bloom_level > 0:
        
        #medium bloom
        if n_patches < 5:
            
            n = round( math.sqrt(max_patch) / 10 )
            
            result = f'''Poppies are blooming at {location}! The coverage level is currently **moderate** 
            and the largest poppy patch right now is about the size of {n} football fields.'''
            st.markdown(result)
            
            suggestion = f'''So grab some water and a friend and visit now for great photo ops!'''
            st.markdown(suggestion)
            
            suggestion = f'''Click {directions} to get directions to the site from your location. 
            And while we're at it, {hikes} are some great nearby hikes recommended by the folks over at {alltrails}.'''
            st.markdown(suggestion)
        
        #large bloom
        else:
            
            n = round( math.sqrt(max_patch) / 10 )
            
            result = f'''The poppy fields are blazing right now at {location}! The coverage level is **high** 
            and the largest poppy patch is the size of {n} football fields!'''
            st.markdown(result)
            
            suggestion = f'''Grab some water and a friend and visit now for great photo ops!'''
            st.markdown(suggestion)
            
            suggestion = f'''Click {directions} to get directions to the site from your location. 
            And while we're at it, {hikes} are some great nearby hikes recommended by the folks over at {alltrails}.'''
            st.markdown(suggestion)
            
    
    
    #May through December
    else:
        
        result = f''' Poppy season is over for {year}. We are sad about this too, 
                 but how about getting your flower fix at the {visit1} or {visit2}? 
                 '''
        st.markdown(result)
        

##url = 'https://www.inaturalist.org/observations?%20quality_grade=any&identifications=any&swlat=34.65275197179807&swlng=-118.54212363125656&nelat=34.80793834080253&nelng=-118.20839253818516&taxon_id=48225&d1=2019-04-01&d2=2019-04-30'
#x = f'''[alt text](https://www.inaturalist.org/observations?%20quality_grade=any&identifications=any&swlat=34.65275197179807&swlng=-118.54212363125656&nelat=34.80793834080253&nelng=-118.20839253818516&taxon_id=48225&d1=2019-04-01&d2=2019-04-30)'''
#st.markdown(x)






