import streamlit as st

import numpy as np
import pandas as pd
import plotly.express as px
import functions as f

meters = {
    'Electricity':              'electricity_cleaned.csv',
    'Natural Gas':              'gas_cleaned.csv',
    'Chilled Water':            'chileedwater_cleaned.csv',
    'Steam':                    'steam_cleaned.csv',
    'Hot Water':                'hotwater_cleaned.csv',
    'Irrigation':               'irrigation_cleaned.csv',
    'Solar':                    'solar_cleaned.csv',
    'Water':                    'water_cleaned.csv'
}

meter_type = st.selectbox(
    'Choose which meter type to analyze:'
    meters.keys()
)
