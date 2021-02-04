import streamlit as st

import numpy as np
import pandas as pd
from plotly import express as px, figure_factory as ff
import functions as f

st.title("BDG2 Site Energy Data Exploration")
st.header("Author: [Zixiao (Shawn) Shi](zixiao.shawn.shi@gmail.com)")

ROOT_URL = 'https://media.githubusercontent.com/media/buds-lab/building-data-genome-project-2/master/data/'
meta_url = ROOT_URL + 'metadata/metadata.csv'
meta_df = f.load_csv(meta_url)
META_COLUMN_DIC = {
    'site_id':                  'Site Name',
    'electricity':              'Electricity',
    'gas':                      'Natural Gas',
    'chilledwater':             'Chilled Water',
    'steam':                    'Steam',
    'hotwater':                 'Hot Water',
    'irrigation':               'Irrigation',
    'solar':                    'Solar',
    'water':                    'Water'
}
meta_df = meta_df.rename(columns = META_COLUMN_DIC)

METERS_DIC = {
    'Electricity':              'electricity_cleaned.csv',
    'Natural Gas':              'gas_cleaned.csv',
    'Chilled Water':            'chilledwater_cleaned.csv',
    'Steam':                    'steam_cleaned.csv',
    'Hot Water':                'hotwater_cleaned.csv',
    'Irrigation':               'irrigation_cleaned.csv',
    'Solar':                    'solar_cleaned.csv',
    'Water':                    'water_cleaned.csv'
}

'''
In this streamlit explorer we examine each site's meter readings from the BDG2 dataset.

[Link to original dataset](https://github.com/buds-lab/building-data-genome-project-2)

Some columns names have been remapped for better readibility.
'''

meter_type = st.selectbox(
    'Choose which meter type to analyze:',
    list(METERS_DIC.keys()),
)

'''
### Number of meters per site
'''
meter_count = meta_df[meta_df[meter_type] == 'Yes'].groupby('Site Name')[meter_type].count()
meter_count_fig = px.bar(
    x=meter_count.index,
    y=meter_count.values,
    labels={
        'x': 'Site',
        'y': meter_type + ' Meters'
    }
)
st.plotly_chart(meter_count_fig)

site_name = st.selectbox(
    'Choose which site to analyze:',
    meta_df['Site Name'].unique()
)
'''
### Site meters overview
'''
meter_url = ROOT_URL + 'meters/cleaned/' + METERS_DIC[meter_type]
meter_df = f.load_csv(meter_url)
meter_df = meter_df.set_index('timestamp')

site_buildings = [col for col in meter_df.columns if site_name == col.split('_')[0]]
meter_df = meter_df[site_buildings]

'''
#### Descriptive statistics
'''
meter_des_df = meter_df.describe()
meter_des_df.loc['%missing', :] = 100.0*meter_df.isnull().sum()/meter_des_df.loc['count', :]
st.dataframe(meter_des_df)

des_col = st.selectbox(
    'Choose which descriptive statistics to plot histogram',
    meter_des_df.index
)

desc_hist = px.histogram(
    meter_des_df.T,
    x = des_col
)
st.plotly_chart(desc_hist)

'''
#### Plot all site meters over time
'''
if st.button('Plot all site meters over time (this may take some time)'):
    with st.spinner('plotting'):
        meter_ts_plot = px.line(
            meter_df,
            x = meter_df.index,
            y = site_buildings
        )
        st.plotly_chart(meter_ts_plot)
    st.success('plot successful')
