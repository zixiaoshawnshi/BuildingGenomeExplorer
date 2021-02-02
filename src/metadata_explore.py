import streamlit as st

import numpy as np
import pandas as pd
import plotly.express as px
import functions as f

st.title("BDG2 Metadata Exploration")
st.header("Author: Zixiao (Shawn) Shi")
'''
In this streamlit explorer we examine the metadata and weather data for the BDG2 dataset.

[Link to original dataset](https://github.com/buds-lab/building-data-genome-project-2)

Some columns names have been remapped for better readibility.
'''
# data loading and preparation
@st.cache
def load_data():
    df = pd.read_csv("https://media.githubusercontent.com/media/buds-lab/building-data-genome-project-2/master/data/metadata/metadata.csv")
    weather_df = pd.read_csv("https://media.githubusercontent.com/media/buds-lab/building-data-genome-project-2/master/data/weather/weather.csv")

    column_dict = {
        'sqm':                  'Square Meters',
        'sqft':                 'Square Feet',
        'yearbuilt':            'Year Built',
        'eui':                  'EUI',
        'site_id':              'Site Name',
        'primaryspaceusage':    'Primary Space Type',
        'timezone':             'Time Zone',
        'lat':                  'latitude',
        'lng':                  'longitude'
    }
    df = df.rename(columns = column_dict)

    weather_column_dict = {
        'site_id':              'Site Name',
        'airTemperature':       'Air Temperature',
        'cloudCoverage':        'Cloud Coverage',
        'dewTemperature':       'Dew Point Temperature',
        'precipDepth1HR':       'Hourly Percipitation Depth',
        'precipDepth6HR':       '6-Hour Percipitation Depth',
        'seaLvlPressure':       'Air Pressure',
        'windDirection':        'Wind Direction',
        'windSpeed':            'Wind Speed',
    }
    weather_df = weather_df.rename(columns = weather_column_dict)

    return df, weather_df

df, weather_df = load_data()

'''
## Number of buildings per site
'''
building_count = df.groupby("Site Name").count()
building_bar_fig = px.bar(
    x=building_count.index,
    y=building_count['building_id'],
    labels={'x': 'Site Name', 'y': 'Buildings'}
)
st.plotly_chart(building_bar_fig)

'''
## Location of the buildings:

'''
map_sites_to_plot = st.multiselect(
    "Choose which site to show on the map:",
    df["Site Name"].unique()
)

map_filter = df["Site Name"].isin(map_sites_to_plot)
st.map(df.loc[map_filter, ['latitude', 'longitude']].dropna())

'''
## Distribution of building attributes:
'''

hist_option_plot_column = st.selectbox(
    'Choose which building attribute to plot the histogram:',
    ["Square Meters", "Square Feet", "Year Built", "EUI"]
)

hist_option_group_column = st.selectbox(
    'Choose which building attribute to group the histogram:',
    ["No Grouping", "Site Name", "Primary Space Type", "Time Zone"]
)

if hist_option_group_column == "No Grouping":
    hist = px.histogram(df, x=hist_option_plot_column)
else:
    hist = px.histogram(df, x=hist_option_plot_column, color = hist_option_group_column)
st.plotly_chart(hist)

'''
## Weather data line plot
'''

weather_ts_plot_colum = st.selectbox(
    "Choose which weather data column to plot:",
    [
        "Air Temperature",
        "Cloud Coverage",
        'Dew Point Temperature',
        'Hourly Percipitation Depth',
        '6-Hour Percipitation Depth',
        'Air Pressure',
        'Wind Direction',
        'Wind Speed',
    ]
)

weahter_ts_sites_to_plot = st.multiselect(
    "Choose which sites to plot weather data for:",
    weather_df["Site Name"].unique()
)

if len(weahter_ts_sites_to_plot) > 0:
    weather_ts_filter = weather_df["Site Name"].isin(weahter_ts_sites_to_plot)
    weather_ts_plot = px.line(
        weather_df.loc[weather_ts_filter, [weather_ts_plot_colum, 'Site Name', 'timestamp']],
        x='timestamp',
        y=weather_ts_plot_colum,
        color='Site Name'
    )
    st.plotly_chart(weather_ts_plot)

'''
## Monthly heating & cooling degree days
'''
hdd_base = st.number_input(
    "Enter the baseline temperature for heating degree days (HDD):",
    value = 10.0,
    step = 0.1
)
cdd_base = st.number_input(
    "Enter the baseline temperature for cooling degree days (CDD):",
    value = 10.0,
    step = 0.1
)
dd_sites_to_plot = st.multiselect(
    "Choose which sites to plot HDD/CDD for:",
    weather_df["Site Name"].unique()
)

if len(dd_sites_to_plot) > 0:
    dd_filter = weather_df["Site Name"].isin(dd_sites_to_plot)
    dd_df = weather_df.loc[dd_filter, ['timestamp', 'Site Name', 'Air Temperature']]
    dd_df['HDD'] = f.calculate_hdd(dd_df, hdd_base, 'Air Temperature')
    dd_df['CDD'] = f.calculate_hdd(dd_df, cdd_base, 'Air Temperature')
    dd_df['timestamp'] = pd.to_datetime(dd_df['timestamp'])
    dd_df = dd_df.set_index('timestamp')
    dd_results = (dd_df.groupby('Site Name').resample('m').sum()/24.0).reset_index()
    hdd_fig = px.bar(dd_results, x='timestamp', y='HDD', color='Site Name', barmode='group')
    st.plotly_chart(hdd_fig)
    cdd_fig = px.bar(dd_results, x='timestamp', y='CDD', color='Site Name', barmode='group')
    st.plotly_chart(cdd_fig)
