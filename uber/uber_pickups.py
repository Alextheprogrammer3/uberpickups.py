import streamlit as st
import pandas as pd
import numpy as np
import requests
import gzip
from io import BytesIO

# Title
st.title('Uber pickups in NYC')

# Constants
DATE_COLUMN = 'date/time'
DATA_URL = 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'

# Function to load data
@st.cache_data
def load_data(nrows):
    response = requests.get(DATA_URL, stream=True, verify=False)
    with gzip.open(BytesIO(response.content)) as f:
        data = pd.read_csv(f, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Load data
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

# Checkbox to show raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Histogram of number of pickups by hour
st.subheader('Number of pickups by hour')
hist_values, bins = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))
st.bar_chart(hist_values)

# Slider to filter data by hour
hour_to_filter = st.slider('Hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# Map of pickups at selected hour
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
